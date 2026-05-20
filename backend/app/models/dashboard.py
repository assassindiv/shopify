from pydantic import Field

from app.models.base import ApiModel


class DashboardMetrics(ApiModel):
    total_chats: int = Field(alias="totalChats")
    ai_resolved: int = Field(alias="aiResolved")
    refunds_prevented: int = Field(alias="refundsPrevented")
    exchanges_suggested: int = Field(alias="exchangesSuggested")
    human_escalations: int = Field(alias="humanEscalations")
    average_response_time: str = Field(alias="averageResponseTime")
    total_returns: int = Field(alias="totalReturns")
    high_risk_flagged: int = Field(alias="highRiskFlagged")
    refund_value_saved: int = Field(alias="refundValueSaved")


class DashboardOverview(ApiModel):
    metrics: DashboardMetrics
