from fastapi import APIRouter

from app.models.ticket import Ticket, TicketCreate, TicketCreateResponse
from app.services.ticket_service import create_ticket, list_tickets


router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=list[Ticket])
def read_tickets() -> list[Ticket]:
    return list_tickets()


@router.post("", response_model=TicketCreateResponse)
def create_support_ticket(payload: TicketCreate) -> TicketCreateResponse:
    return create_ticket(payload)
