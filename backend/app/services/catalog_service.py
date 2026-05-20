from app.core.errors import AppError
from app.models.product import Product
from app.services.data_store import load_json


def list_products() -> list[Product]:
    return [Product.model_validate(product) for product in load_json("products.json")]


def get_product(product_id: str) -> Product:
    for product in list_products():
        if product.id == product_id:
            return product

    raise AppError(
        code="PRODUCT_NOT_FOUND",
        message="No product was found for the provided product ID.",
        status_code=404,
    )
