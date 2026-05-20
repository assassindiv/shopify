from fastapi import APIRouter

from app.models.ticket import Ticket, TicketCreate, TicketCreateResponse, TicketUpdate
from app.services.ticket_service import create_ticket, list_tickets, update_ticket


router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=list[Ticket])
def read_tickets() -> list[Ticket]:
    return list_tickets()


@router.post("", response_model=TicketCreateResponse)
def create_support_ticket(payload: TicketCreate) -> TicketCreateResponse:
    return create_ticket(payload)


@router.patch("/{ticket_id}", response_model=Ticket)
def update_support_ticket(ticket_id: str, payload: TicketUpdate) -> Ticket:
    return update_ticket(ticket_id, payload)
