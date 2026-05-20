from fastapi import APIRouter

from app.models.product import Product
from app.services.catalog_service import get_product


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: str) -> Product:
    return get_product(product_id)
