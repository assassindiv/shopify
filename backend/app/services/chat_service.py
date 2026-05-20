import json

from app.core.config import GROQ_MODEL
from app.models.chat import ChatExtraction, ChatRequest, ChatResponse
from app.models.return_request import ReturnCheckRequest
from app.services.catalog_service import get_product, list_products
from app.services.groq_service import groq_chat_json
from app.services.order_service import get_order
from app.services.return_service import check_return


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

Set needsMoreInfo true when a return/refund/exchange request is missing orderId or customerEmail.
Use null for missing strings. Do not invent values.
"""

RESPONSE_PROMPT = """
You are ReturnShield, a Shopify-native customer support agent.
Write a concise, helpful customer-facing reply.

Rules:
- Do not change the eligibility, risk score, risk level, risk reasons, ticket ID, or recommended action.
- If a return decision is provided, explain the next step clearly.
- If tool context is provided, use only that context for order, product, and policy facts.
- If information is missing, ask only for what is missing.
- Keep the tone professional and calm.
- Return only JSON with this shape: {"message": "..."}.
"""

POLICY_CONTEXT = {
    "returnPolicy": "Most returnable items can be returned within the product return window if unused and in acceptable condition.",
    "refundPolicy": "Refunds are approved after eligibility and risk checks. High-risk refunds require human review or evidence.",
    "damagePolicy": "Damaged-item claims may require photo or video proof before refund approval.",
    "exchangePolicy": "Size and fit issues should prioritize exchange when stock is available.",
    "saleItemPolicy": "Sale items are not usually refundable unless damaged or the wrong item was delivered.",
}


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
        tool_context = {"policies": POLICY_CONTEXT}
    elif extraction.intent == "product_question":
        tool_context = {
            "products": [
                product.model_dump(by_alias=True) for product in list_products()
            ]
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

    return ChatResponse(
        message=response_raw.get("message", "I can help with that."),
        intent=extraction.intent,
        extraction=extraction,
        returnDecision=return_decision,
        aiModel=GROQ_MODEL,
    )
