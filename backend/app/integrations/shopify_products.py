from app.integrations.shopify_client import shopify_graphql, shopify_is_configured
from app.services.catalog_service import list_products


PRODUCTS_QUERY = """
query ReturnShieldProducts($first: Int!) {
  products(first: $first) {
    edges {
      node {
        id
        title
        productType
        totalInventory
        variants(first: 5) {
          edges {
            node {
              id
              title
              price
              inventoryQuantity
            }
          }
        }
      }
    }
  }
}
"""


async def get_shopify_products(first: int = 3) -> dict:
    if not shopify_is_configured():
        return {
            "source": "synthetic",
            "products": [
                {
                    "id": product.id,
                    "title": product.name,
                    "productType": product.category,
                    "totalInventory": product.stock,
                    "variants": [],
                }
                for product in list_products()[:first]
            ],
        }

    data = await shopify_graphql(PRODUCTS_QUERY, {"first": first})
    products = [
        edge["node"]
        for edge in data.get("products", {}).get("edges", [])
    ]
    return {"source": "shopify", "products": products}
