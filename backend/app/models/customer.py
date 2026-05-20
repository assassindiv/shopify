from pydantic import Field

from app.models.base import ApiModel


class Customer(ApiModel):
    id: str
    name: str
    email: str
    returns_last_60_days: int = Field(alias="returnsLast60Days")
    returns_last_45_days: int = Field(alias="returnsLast45Days")
    previous_damage_claims: int = Field(alias="previousDamageClaims")
    previous_refund_claims: int = Field(alias="previousRefundClaims")
