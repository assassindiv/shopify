from app.core.errors import AppError
from app.core.errors import AppError
from app.models.ticket import Ticket, TicketCreate, TicketCreateResponse, TicketUpdate
from app.services.data_store import load_json, save_json
from app.services.order_service import get_customer


_tickets: list[Ticket] = [
    Ticket.model_validate(ticket) for ticket in load_json("tickets.json")
]


def _save_tickets() -> None:
    save_json(
        "tickets.json",
        [ticket.model_dump(by_alias=True) for ticket in _tickets],
    )


def list_tickets() -> list[Ticket]:
    return _tickets


def get_ticket(ticket_id: str) -> Ticket:
    for ticket in _tickets:
        if ticket.id == ticket_id:
            return ticket

    raise AppError(
        code="TICKET_NOT_FOUND",
        message="No ticket was found for the provided ticket ID.",
        status_code=404,
    )


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
        evidenceProvided=False,
    )
    _tickets.append(ticket)
    _save_tickets()

    return TicketCreateResponse(id=ticket.id, status=ticket.status)


def update_ticket(ticket_id: str, payload: TicketUpdate) -> Ticket:
    ticket = get_ticket(ticket_id)

    if payload.status is not None:
        ticket.status = payload.status
    if payload.suggested_action is not None:
        ticket.suggested_action = payload.suggested_action
    if payload.evidence_provided is not None:
        ticket.evidence_provided = payload.evidence_provided
        if payload.evidence_provided and ticket.status == "Evidence Required":
            ticket.status = "Human Review"

    _save_tickets()
    return ticket


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
