from pydantic import Field

from app.models.base import ApiModel


class RiskScoreRequest(ApiModel):
    order_id: str = Field(alias="orderId")
    reason: str
    photo_proof_provided: bool = Field(default=False, alias="photoProofProvided")


class RiskScoreResponse(ApiModel):
    risk_score: int = Field(alias="riskScore")
    risk_level: str = Field(alias="riskLevel")
    reasons: list[str]
    recommended_action: str = Field(alias="recommendedAction")


class ReturnCheckRequest(ApiModel):
    order_id: str = Field(alias="orderId")
    customer_email: str = Field(alias="customerEmail")
    reason: str
    photo_proof_provided: bool = Field(default=False, alias="photoProofProvided")


class ReturnCheckResponse(ApiModel):
    eligible: bool
    return_window_days: int = Field(alias="returnWindowDays")
    days_since_delivery: int | None = Field(alias="daysSinceDelivery")
    reason: str
    risk_score: int = Field(alias="riskScore")
    risk_level: str = Field(alias="riskLevel")
    risk_reasons: list[str] = Field(alias="riskReasons")
    recommended_action: str = Field(alias="recommendedAction")
    customer_message: str = Field(alias="customerMessage")
    ticket_id: str | None = Field(default=None, alias="ticketId")
