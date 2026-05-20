from fastapi import APIRouter

from app.models.return_request import RiskScoreRequest, RiskScoreResponse
from app.services.catalog_service import get_product
from app.services.order_service import get_customer, get_order
from app.services.return_service import _days_since_delivery
from app.services.risk_service import calculate_risk


router = APIRouter(prefix="/risk-score", tags=["risk"])


@router.post("", response_model=RiskScoreResponse)
def calculate_return_risk(payload: RiskScoreRequest) -> RiskScoreResponse:
    order = get_order(payload.order_id)
    product = get_product(order.product_id)
    customer = get_customer(order.customer_id)

    return calculate_risk(
        order=order,
        product=product,
        customer=customer,
        reason=payload.reason,
        photo_proof_provided=payload.photo_proof_provided,
        days_since_delivery=_days_since_delivery(order.delivered_at),
    )
