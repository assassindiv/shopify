from pydantic import Field

from app.models.base import ApiModel


class Ticket(ApiModel):
    id: str
    order_id: str = Field(alias="orderId")
    customer_id: str = Field(alias="customerId")
    customer_name: str = Field(alias="customerName")
    issue: str
    risk_level: str = Field(alias="riskLevel")
    risk_score: int = Field(alias="riskScore")
    suggested_action: str = Field(alias="suggestedAction")
    status: str
    evidence_provided: bool = Field(default=False, alias="evidenceProvided")


class TicketCreate(ApiModel):
    order_id: str = Field(alias="orderId")
    customer_id: str = Field(alias="customerId")
    issue: str
    risk_level: str = Field(alias="riskLevel")
    risk_score: int = Field(alias="riskScore")
    suggested_action: str = Field(alias="suggestedAction")


class TicketCreateResponse(ApiModel):
    id: str
    status: str


class TicketUpdate(ApiModel):
    status: str | None = None
    suggested_action: str | None = Field(default=None, alias="suggestedAction")
    evidence_provided: bool | None = Field(default=None, alias="evidenceProvided")
