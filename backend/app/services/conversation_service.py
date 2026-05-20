from app.core.errors import AppError
from app.models.conversation import Conversation, ConversationMessage, now_iso
from app.services.data_store import load_json, save_json


_conversations: list[Conversation] = [
    Conversation.model_validate(conversation)
    for conversation in load_json("conversations.json")
]


def _save_conversations() -> None:
    save_json(
        "conversations.json",
        [conversation.model_dump(by_alias=True) for conversation in _conversations],
    )


def list_conversations() -> list[Conversation]:
    return sorted(_conversations, key=lambda item: item.updated_at, reverse=True)


def get_conversation(conversation_id: str) -> Conversation:
    for conversation in _conversations:
        if conversation.id == conversation_id:
            return conversation

    raise AppError(
        code="CONVERSATION_NOT_FOUND",
        message="No conversation was found for the provided conversation ID.",
        status_code=404,
    )


def get_or_create_conversation(conversation_id: str | None) -> Conversation:
    if conversation_id:
        for conversation in _conversations:
            if conversation.id == conversation_id:
                return conversation

    return create_conversation()


def create_conversation(customer_email: str | None = None) -> Conversation:
    timestamp = now_iso()
    conversation = Conversation(
        id=f"C-{1000 + len(_conversations) + 1}",
        customerEmail=customer_email,
        orderId=None,
        intent="unknown",
        status="Open",
        riskLevel=None,
        ticketId=None,
        updatedAt=timestamp,
        messages=[],
    )
    _conversations.append(conversation)
    _save_conversations()
    return conversation


def append_message(conversation_id: str, role: str, content: str) -> Conversation:
    conversation = get_conversation(conversation_id)
    timestamp = now_iso()
    conversation.messages.append(
        ConversationMessage(role=role, content=content, createdAt=timestamp)
    )
    conversation.updated_at = timestamp
    _save_conversations()
    return conversation


def record_chat_turn(
    *,
    customer_message: str,
    assistant_message: str,
    intent: str,
    customer_email: str | None,
    order_id: str | None,
    risk_level: str | None,
    ticket_id: str | None,
    conversation_id: str | None = None,
) -> Conversation:
    conversation = get_or_create_conversation(conversation_id) if conversation_id else None

    if conversation is None and (customer_email or order_id):
        conversation = next(
            (
                item
                for item in _conversations
                if (customer_email and item.customer_email == customer_email)
                or (order_id and item.order_id == order_id)
            ),
            None,
        )

    timestamp = now_iso()
    if conversation is None:
        conversation = Conversation(
            id=f"C-{1000 + len(_conversations) + 1}",
            customerEmail=customer_email,
            orderId=order_id,
            intent=intent,
            status="Open",
            riskLevel=risk_level,
            ticketId=ticket_id,
            updatedAt=timestamp,
            messages=[],
        )
        _conversations.append(conversation)

    conversation.intent = intent
    conversation.customer_email = customer_email or conversation.customer_email
    conversation.order_id = order_id or conversation.order_id
    conversation.risk_level = risk_level or conversation.risk_level
    conversation.ticket_id = ticket_id or conversation.ticket_id
    conversation.status = "Escalated" if risk_level == "High" else "Open"
    conversation.updated_at = timestamp
    conversation.messages.extend(
        [
            ConversationMessage(
                role="customer",
                content=customer_message,
                createdAt=timestamp,
            ),
            ConversationMessage(
                role="assistant",
                content=assistant_message,
                createdAt=timestamp,
            ),
        ]
    )

    _save_conversations()
    return conversation


def attach_evidence(
    *,
    conversation_id: str,
    note: str | None,
) -> Conversation:
    message = "Customer uploaded photo/video proof."
    if note:
        message = f"{message} Note: {note}"
    conversation = append_message(conversation_id, "customer", message)
    conversation.status = "Evidence Submitted"
    if conversation.ticket_id:
        from app.models.ticket import TicketUpdate
        from app.services.ticket_service import update_ticket

        update_ticket(
            conversation.ticket_id,
            TicketUpdate(evidenceProvided=True, status="Human Review"),
        )
    _save_conversations()
    return conversation
