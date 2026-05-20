from datetime import date

from app.core.config import DEMO_TODAY
from app.core.errors import AppError
from app.models.return_request import ReturnCheckRequest, ReturnCheckResponse
from app.services.catalog_service import get_product
from app.services.order_service import get_customer_by_email, get_order
from app.services.risk_service import calculate_risk
from app.services.ticket_service import create_return_ticket


RETURN_REASON_LABELS = {
    "size_issue": "Size issue",
    "damaged_item": "Damaged item",
    "wrong_item": "Wrong item received",
    "late_delivery": "Late delivery",
    "buyer_regret": "Buyer regret",
    "not_as_described": "Product not as described",
    "missing_item": "Missing item",
    "repeated_return_pattern": "Repeated return pattern",
}


def _days_since_delivery(delivered_at: str | None) -> int | None:
    if delivered_at is None:
        return None

    delivered_date = date.fromisoformat(delivered_at)
    return (DEMO_TODAY - delivered_date).days


def _build_customer_message(
    *,
    eligible: bool,
    reason: str,
    risk_level: str,
    recommended_action: str,
) -> str:
    if not eligible:
        return (
            "I checked this order and it is not eligible for an automatic return. "
            "I can escalate this to our support team for review."
        )

    if reason == "damaged_item" and risk_level in {"Medium", "High"}:
        return (
            "I can help with this. Since the item is within the return window, "
            "your request is eligible for review. Because this account has multiple "
            "recent damage-related refund claims, I need a photo of the damaged "
            "product before approving a refund. Once uploaded, I can offer a "
            "replacement, store credit, or escalate this to our support team."
        )

    return (
        "Your request is eligible based on the current return policy. "
        f"Recommended next step: {recommended_action}."
    )


def check_return(payload: ReturnCheckRequest) -> ReturnCheckResponse:
    order = get_order(payload.order_id)
    customer = get_customer_by_email(payload.customer_email)

    if customer.id != order.customer_id:
        raise AppError(
            code="CUSTOMER_ORDER_MISMATCH",
            message="The provided email does not match this order.",
            status_code=403,
        )

    product = get_product(order.product_id)
    days_since_delivery = _days_since_delivery(order.delivered_at)
    delivered = order.status.lower() == "delivered"
    within_window = (
        days_since_delivery is not None
        and days_since_delivery <= product.return_window_days
    )
    eligible = delivered and product.returnable and within_window

    risk = calculate_risk(
        order=order,
        product=product,
        customer=customer,
        reason=payload.reason,
        photo_proof_provided=payload.photo_proof_provided,
        days_since_delivery=days_since_delivery,
    )

    ticket_id: str | None = None
    if risk.risk_level != "Low" or not eligible:
        ticket = create_return_ticket(
            order_id=order.id,
            customer_id=customer.id,
            issue=RETURN_REASON_LABELS.get(payload.reason, payload.reason),
            risk_level=risk.risk_level,
            risk_score=risk.risk_score,
            suggested_action=risk.recommended_action,
        )
        ticket_id = ticket.id

    return ReturnCheckResponse(
        eligible=eligible,
        returnWindowDays=product.return_window_days,
        daysSinceDelivery=days_since_delivery,
        reason=payload.reason,
        riskScore=risk.risk_score,
        riskLevel=risk.risk_level,
        riskReasons=risk.reasons,
        recommendedAction=risk.recommended_action,
        customerMessage=_build_customer_message(
            eligible=eligible,
            reason=payload.reason,
            risk_level=risk.risk_level,
            recommended_action=risk.recommended_action,
        ),
        ticketId=ticket_id,
    )
