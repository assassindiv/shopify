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
