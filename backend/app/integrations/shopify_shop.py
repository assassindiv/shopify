from app.core.config import SHOPIFY_API_VERSION, SHOPIFY_STORE_NAME
from app.integrations.shopify_client import shopify_graphql, shopify_is_configured


SHOP_QUERY = """
query ReturnShieldShop {
  shop {
    name
    myshopifyDomain
  }
}
"""


async def get_shopify_shop() -> dict:
    if not shopify_is_configured():
        return {
            "source": "synthetic",
            "shop": {
                "name": "Synthetic ReturnShield Dev Store",
                "myshopifyDomain": (
                    f"{SHOPIFY_STORE_NAME}.myshopify.com"
                    if SHOPIFY_STORE_NAME
                    else "synthetic-dev-store.myshopify.com"
                ),
                "apiVersion": SHOPIFY_API_VERSION,
            },
        }

    data = await shopify_graphql(SHOP_QUERY)
    return {"source": "shopify", "shop": data.get("shop")}
