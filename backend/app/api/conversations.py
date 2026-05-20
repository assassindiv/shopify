from fastapi import APIRouter

from app.models.conversation import (
    Conversation,
    ConversationCreate,
    ConversationReply,
    EvidenceSubmit,
)
from app.services.conversation_service import (
    append_message,
    attach_evidence,
    create_conversation,
    get_conversation,
    get_or_create_conversation,
    list_conversations,
)


router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("", response_model=list[Conversation])
def read_conversations() -> list[Conversation]:
    return list_conversations()


@router.post("", response_model=Conversation)
def start_conversation(payload: ConversationCreate) -> Conversation:
    return create_conversation(payload.customer_email)


@router.get("/{conversation_id}", response_model=Conversation)
def read_conversation(conversation_id: str) -> Conversation:
    return get_or_create_conversation(conversation_id)


@router.post("/{conversation_id}/messages", response_model=Conversation)
def reply_to_conversation(
    conversation_id: str,
    payload: ConversationReply,
) -> Conversation:
    return append_message(conversation_id, payload.role, payload.content)


@router.post("/{conversation_id}/evidence", response_model=Conversation)
def submit_evidence(
    conversation_id: str,
    payload: EvidenceSubmit,
) -> Conversation:
    return attach_evidence(conversation_id=conversation_id, note=payload.note)
