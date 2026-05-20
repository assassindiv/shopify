import json

from app.core.config import GROQ_MODEL
from app.models.chat import ChatExtraction, ChatRequest, ChatResponse
from app.models.return_request import ReturnCheckRequest
from app.services.catalog_service import get_product, list_products
from app.services.conversation_service import record_chat_turn
from app.services.groq_service import groq_chat_json
from app.services.order_service import get_order
from app.services.return_service import check_return
from app.services.data_store import load_json


def _matching_products(message: str) -> list[dict]:
    normalized = message.lower()
    matches = []

    for product in list_products():
        terms = set(product.name.lower().split())
        terms.add(product.category.lower())
        attributes = product.attributes or {}
        for value in attributes.values():
            if isinstance(value, str):
                terms.update(value.lower().replace("/", " ").split())
        useful_terms = {term.strip(".,!?") for term in terms if len(term) >= 4}

        if any(term in normalized for term in useful_terms):
            matches.append(product.model_dump(by_alias=True))

    return matches


EXTRACTION_PROMPT = """
You are the intent extraction layer for ReturnShield, a Shopify support agent.
Return only JSON.

Allowed intents:
- order_tracking
- product_question
- policy_question
- return_request
- refund_request
- exchange_request
- unknown

Allowed return reasons:
- size_issue
- damaged_item
- wrong_item
- late_delivery
- buyer_regret
- not_as_described
- missing_item
- repeated_return_pattern

Extract:
- intent
- orderId
- customerEmail
- reason
- photoProofProvided
- needsMoreInfo

Use the latest message and conversation history together. If the latest message only
contains missing details like order ID or email, infer the intent and reason from the
previous customer messages.

Set needsMoreInfo true when a return/refund/exchange request is missing orderId or customerEmail.
Use null for missing strings. Do not invent values.
"""

RESPONSE_PROMPT = """
You are ReturnShield, a Shopify-native customer support agent.
Write a concise, helpful customer-facing reply from the classified intent, extracted fields,
and tool results.

Rules:
- Do not change the eligibility, risk score, risk level, risk reasons, ticket ID, or recommended action.
- If a return decision is provided, explain the next step clearly.
- If tool context is provided, use only that context for order, product, and policy facts.
- For product questions, if the customer asks about a product or detail not present in the catalog context, say you do not have that catalog information. Do not answer using a different product.
- For policy questions, mention the relevant policy title when possible.
- If information is missing, ask only for what is missing.
- Do not copy a prewritten template verbatim. Generate a natural response for this exact customer message.
- Mention evidence, escalation, exchange, replacement, refund, or store credit only when supported by the tool result.
- Keep the tone professional and calm.
- Return only JSON with this shape: {"message": "..."}.
"""


async def handle_chat(payload: ChatRequest) -> ChatResponse:
    extraction_raw = await groq_chat_json(
        system_prompt=EXTRACTION_PROMPT,
        user_prompt=json.dumps(
            {
                "latestMessage": payload.message,
                "history": [message.model_dump() for message in payload.history[-6:]],
            }
        ),
    )
    extraction = ChatExtraction.model_validate(extraction_raw)

    return_decision = None
    tool_context = None
    if (
        extraction.intent in {"return_request", "refund_request", "exchange_request"}
        and extraction.order_id
        and extraction.customer_email
    ):
        return_decision = check_return(
            ReturnCheckRequest(
                orderId=extraction.order_id,
                customerEmail=extraction.customer_email,
                reason=extraction.reason or "buyer_regret",
                photoProofProvided=extraction.photo_proof_provided,
            )
        )
    elif extraction.intent == "order_tracking" and extraction.order_id:
        order = get_order(extraction.order_id)
        product = get_product(order.product_id)
        tool_context = {
            "order": order.model_dump(by_alias=True),
            "product": product.model_dump(by_alias=True),
        }
    elif extraction.intent == "policy_question":
        tool_context = {"policies": load_json("policies.json")}
    elif extraction.intent == "product_question":
        matches = _matching_products(payload.message)
        tool_context = {
            "products": matches,
            "catalogNote": (
                "No matching product was found in the store catalog. "
                "Tell the customer you do not have enough catalog data to answer."
                if not matches
                else "Use only these matching catalog products."
            ),
        }

    response_raw = await groq_chat_json(
        system_prompt=RESPONSE_PROMPT,
        user_prompt=json.dumps(
            {
                "latestMessage": payload.message,
                "extraction": extraction.model_dump(by_alias=True),
                "toolContext": tool_context,
                "returnDecision": (
                    return_decision.model_dump(by_alias=True)
                    if return_decision
                    else None
                ),
            }
        ),
        temperature=0.2,
    )

    message = response_raw.get("message", "I can help with that.")
    conversation = record_chat_turn(
        customer_message=payload.message,
        assistant_message=message,
        intent=extraction.intent,
        customer_email=extraction.customer_email,
        order_id=extraction.order_id,
        risk_level=return_decision.risk_level if return_decision else None,
        ticket_id=return_decision.ticket_id if return_decision else None,
        conversation_id=payload.conversation_id,
    )

    return ChatResponse(
        message=message,
        conversationId=conversation.id,
        intent=extraction.intent,
        extraction=extraction,
        returnDecision=return_decision,
        aiModel=GROQ_MODEL,
    )
