from app.core.errors import AppError
from app.models.ticket import Ticket, TicketCreate, TicketCreateResponse
from app.services.data_store import load_json
from app.services.order_service import get_customer


_tickets: list[Ticket] = [
    Ticket.model_validate(ticket) for ticket in load_json("tickets.json")
]


def list_tickets() -> list[Ticket]:
    return _tickets


def create_ticket(payload: TicketCreate) -> TicketCreateResponse:
    existing = next(
        (ticket for ticket in _tickets if ticket.order_id == payload.order_id),
        None,
    )
    if existing:
        return TicketCreateResponse(id=existing.id, status=existing.status)

    customer = get_customer(payload.customer_id)
    ticket_number = 100 + len(_tickets) + 3
    status = "Evidence Required" if payload.risk_level != "Low" else "Open"
    ticket = Ticket(
        id=f"T-{ticket_number}",
        orderId=payload.order_id,
        customerId=payload.customer_id,
        customerName=customer.name,
        issue=payload.issue,
        riskLevel=payload.risk_level,
        riskScore=payload.risk_score,
        suggestedAction=payload.suggested_action,
        status=status,
    )
    _tickets.append(ticket)

    return TicketCreateResponse(id=ticket.id, status=ticket.status)


def create_return_ticket(
    *,
    order_id: str,
    customer_id: str,
    issue: str,
    risk_level: str,
    risk_score: int,
    suggested_action: str,
) -> TicketCreateResponse:
    if risk_level == "Low":
        raise AppError(
            code="TICKET_NOT_REQUIRED",
            message="Low-risk return requests do not require a ticket.",
        )

    return create_ticket(
        TicketCreate(
            orderId=order_id,
            customerId=customer_id,
            issue=issue,
            riskLevel=risk_level,
            riskScore=risk_score,
            suggestedAction=suggested_action,
        )
    )
