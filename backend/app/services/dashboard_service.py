from app.models.dashboard import DashboardMetrics, DashboardOverview
from app.services.ticket_service import list_tickets


BASE_TOTAL_CHATS = 1284
BASE_AI_RESOLVED = 1091
BASE_REFUNDS_PREVENTED = 240000
BASE_EXCHANGES_SUGGESTED = 132
BASE_TOTAL_RETURNS = 347


def get_dashboard_overview() -> DashboardOverview:
    tickets = list_tickets()
    high_risk_tickets = [ticket for ticket in tickets if ticket.risk_level == "High"]
    medium_or_high_tickets = [
        ticket for ticket in tickets if ticket.risk_level in {"Medium", "High"}
    ]
    exchange_tickets = [
        ticket
        for ticket in tickets
        if "exchange" in ticket.suggested_action.lower()
        or "exchange" in ticket.issue.lower()
    ]
    prevented_value = sum(ticket.risk_score * 100 for ticket in medium_or_high_tickets)

    return DashboardOverview(
        metrics=DashboardMetrics(
            totalChats=BASE_TOTAL_CHATS + len(tickets),
            aiResolved=BASE_AI_RESOLVED + max(0, len(tickets) - len(high_risk_tickets)),
            refundsPrevented=BASE_REFUNDS_PREVENTED + prevented_value,
            exchangesSuggested=BASE_EXCHANGES_SUGGESTED + len(exchange_tickets),
            humanEscalations=len(high_risk_tickets),
            averageResponseTime="3.2s",
            totalReturns=BASE_TOTAL_RETURNS + len(tickets),
            highRiskFlagged=len(high_risk_tickets),
            refundValueSaved=180000 + prevented_value,
        )
    )
