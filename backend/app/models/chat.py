from typing import Literal

from pydantic import Field, field_validator

from app.models.base import ApiModel
from app.models.return_request import ReturnCheckResponse


ChatIntent = Literal[
    "order_tracking",
    "product_question",
    "policy_question",
    "return_request",
    "refund_request",
    "exchange_request",
    "unknown",
]


class ChatMessage(ApiModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(ApiModel):
    message: str
    conversation_id: str | None = Field(default=None, alias="conversationId")
    history: list[ChatMessage] = Field(default_factory=list)


class ChatExtraction(ApiModel):
    intent: ChatIntent
    order_id: str | None = Field(default=None, alias="orderId")
    customer_email: str | None = Field(default=None, alias="customerEmail")
    reason: str | None = None
    photo_proof_provided: bool = Field(default=False, alias="photoProofProvided")
    needs_more_info: bool = Field(default=False, alias="needsMoreInfo")

    @field_validator("photo_proof_provided", "needs_more_info", mode="before")
    @classmethod
    def default_missing_boolean(cls, value: object) -> bool:
        if value is None:
            return False
        return bool(value)


class ChatResponse(ApiModel):
    message: str
    conversation_id: str = Field(alias="conversationId")
    intent: ChatIntent
    extraction: ChatExtraction
    return_decision: ReturnCheckResponse | None = Field(
        default=None,
        alias="returnDecision",
    )
    ai_provider: str = Field(default="groq", alias="aiProvider")
    ai_model: str = Field(alias="aiModel")
