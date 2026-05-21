from fastapi import APIRouter

from app.integrations.shopify_products import get_shopify_products
from app.integrations.shopify_shop import get_shopify_shop


router = APIRouter(prefix="/shopify", tags=["shopify"])


@router.get("/shop")
async def read_shopify_shop() -> dict:
    return await get_shopify_shop()


@router.get("/products")
async def read_shopify_products(first: int = 3) -> dict:
    return await get_shopify_products(first=first)
