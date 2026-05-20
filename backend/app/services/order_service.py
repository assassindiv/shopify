from app.core.errors import AppError
from app.models.customer import Customer
from app.models.order import Order
from app.services.data_store import load_json


def list_orders() -> list[Order]:
    return [Order.model_validate(order) for order in load_json("orders.json")]


def list_customers() -> list[Customer]:
    return [Customer.model_validate(customer) for customer in load_json("customers.json")]


def get_order(order_id: str) -> Order:
    for order in list_orders():
        if order.id == order_id:
            return order

    raise AppError(
        code="ORDER_NOT_FOUND",
        message="No order was found for the provided order ID.",
        status_code=404,
    )


def get_customer(customer_id: str) -> Customer:
    for customer in list_customers():
        if customer.id == customer_id:
            return customer

    raise AppError(
        code="CUSTOMER_NOT_FOUND",
        message="No customer was found for the provided customer ID.",
        status_code=404,
    )


def get_customer_by_email(email: str) -> Customer:
    normalized_email = email.strip().lower()

    for customer in list_customers():
        if customer.email.lower() == normalized_email:
            return customer

    raise AppError(
        code="CUSTOMER_NOT_FOUND",
        message="No customer was found for the provided email.",
        status_code=404,
    )
