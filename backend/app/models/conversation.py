from datetime import datetime
from typing import Literal

from pydantic import Field

from app.models.base import ApiModel


class ConversationMessage(ApiModel):
    role: Literal["customer", "assistant", "merchant", "system"]
    content: str
    created_at: str = Field(alias="createdAt")


class Conversation(ApiModel):
    id: str
    customer_email: str | None = Field(default=None, alias="customerEmail")
    order_id: str | None = Field(default=None, alias="orderId")
    intent: str
    status: str
    risk_level: str | None = Field(default=None, alias="riskLevel")
    ticket_id: str | None = Field(default=None, alias="ticketId")
    updated_at: str = Field(alias="updatedAt")
    messages: list[ConversationMessage]


class ConversationCreate(ApiModel):
    customer_email: str | None = Field(default=None, alias="customerEmail")


class ConversationReply(ApiModel):
    role: Literal["merchant", "assistant", "system"]
    content: str


class EvidenceSubmit(ApiModel):
    note: str | None = None
    photo_proof_provided: bool = Field(default=True, alias="photoProofProvided")


def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
