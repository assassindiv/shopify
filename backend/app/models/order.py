from pydantic import Field

from app.models.base import ApiModel


class Order(ApiModel):
    id: str
    customer_id: str = Field(alias="customerId")
    product_id: str = Field(alias="productId")
    status: str
    delivered_at: str | None = Field(alias="deliveredAt")
    amount: int
