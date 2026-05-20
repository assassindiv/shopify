from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.models.return_request import RiskScoreResponse


def classify_risk(score: int) -> str:
    if score <= 30:
        return "Low"
    if score <= 60:
        return "Medium"
    return "High"


def recommended_action_for(risk_level: str, reason: str) -> str:
    if risk_level == "High":
        return "Request photo proof and escalate if unclear"
    if risk_level == "Medium":
        return "Ask for more evidence"
    if reason == "size_issue":
        return "Recommend exchange"
    if reason == "damaged_item":
        return "Approve replacement or refund"
    return "Auto-approve"


def calculate_risk(
    *,
    order: Order,
    product: Product,
    customer: Customer,
    reason: str,
    photo_proof_provided: bool,
    days_since_delivery: int | None,
) -> RiskScoreResponse:
    score = 0
    reasons: list[str] = []

    if customer.returns_last_60_days > 3:
        score += 20
        reasons.append(
            f"Customer has {customer.returns_last_60_days} returns in the last 60 days"
        )

    if order.amount > 5000 or product.price > 5000:
        score += 20
        reasons.append("Item value is above INR 5000")

    if reason == "damaged_item" and not photo_proof_provided:
        score += 15
        reasons.append("Damage claim has no photo proof")

    if days_since_delivery is not None and days_since_delivery >= product.return_window_days:
        score += 15
        reasons.append("Return was requested on the final return-window day")

    if customer.previous_refund_claims >= 2 or customer.previous_damage_claims >= 2:
        score += 20
        reasons.append("Customer has repeated damaged-item claims")

    if product.high_risk_category:
        score += 10
        reasons.append(f"{product.category} is a high-risk return category")

    risk_level = classify_risk(score)

    return RiskScoreResponse(
        riskScore=score,
        riskLevel=risk_level,
        reasons=reasons,
        recommendedAction=recommended_action_for(risk_level, reason),
    )
