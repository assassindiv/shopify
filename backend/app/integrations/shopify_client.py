import httpx

from app.core.config import (
    SHOPIFY_ACCESS_TOKEN,
    SHOPIFY_API_VERSION,
    SHOPIFY_STORE_NAME,
)
from app.core.errors import AppError


def shopify_is_configured() -> bool:
    return bool(SHOPIFY_STORE_NAME and SHOPIFY_ACCESS_TOKEN)


def shopify_graphql_endpoint() -> str:
    store = SHOPIFY_STORE_NAME or ""
    if store.endswith(".myshopify.com"):
        host = store
    else:
        host = f"{store}.myshopify.com"
    return f"https://{host}/admin/api/{SHOPIFY_API_VERSION}/graphql.json"


async def shopify_graphql(query: str, variables: dict | None = None) -> dict:
    if not shopify_is_configured():
        raise AppError(
            code="SHOPIFY_NOT_CONFIGURED",
            message="Shopify credentials are not configured; using synthetic data for demo.",
            status_code=503,
        )

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                shopify_graphql_endpoint(),
                headers={
                    "Content-Type": "application/json",
                    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN or "",
                },
                json={"query": query, "variables": variables or {}},
            )
    except httpx.HTTPError as exc:
        raise AppError(
            code="SHOPIFY_REQUEST_FAILED",
            message="Could not reach Shopify Admin GraphQL API.",
            status_code=502,
        ) from exc

    if response.status_code >= 400:
        raise AppError(
            code="SHOPIFY_API_ERROR",
            message=f"Shopify returned status {response.status_code}.",
            status_code=502,
        )

    data = response.json()
    if data.get("errors"):
        raise AppError(
            code="SHOPIFY_GRAPHQL_ERROR",
            message="Shopify returned GraphQL errors.",
            status_code=502,
        )

    return data.get("data", {})
