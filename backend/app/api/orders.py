from fastapi import APIRouter

from app.models.order import Order
from app.services.order_service import get_order


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/{order_id}", response_model=Order)
def read_order(order_id: str) -> Order:
    return get_order(order_id)
