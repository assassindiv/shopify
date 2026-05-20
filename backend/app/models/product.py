from pydantic import Field

from app.models.base import ApiModel


class Product(ApiModel):
    id: str
    name: str
    category: str
    price: int
    returnable: bool
    return_window_days: int = Field(alias="returnWindowDays")
    stock: int
    high_risk_category: bool = Field(default=False, alias="highRiskCategory")
