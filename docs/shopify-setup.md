# Shopify Setup And Integration Plan

## Challenge-Aligned Setup

The MVP uses synthetic Shopify-style data. This is intentional: the focus is on product thinking, decision workflows, and engineering quality rather than access to a real merchant store.

For a real Shopify integration, the setup would be:

1. Create a free Shopify Partner account at `partners.shopify.com`.
2. Create a development store from the Partner Dashboard.
3. Populate the store with synthetic product data for the chosen category.
4. Create a custom app in the development store.
5. Enable Admin API access for the app.
6. Store Shopify credentials in environment variables.

## Useful Shopify Resources

- Shopify Admin GraphQL API: `shopify.dev/docs/api/admin-graphql`
- Shopify Storefront API: `shopify.dev/docs/api/storefront`
- Shopify App Development: `shopify.dev/docs/apps`
- Shopify Agentic Commerce context: `shopify.com/agentic-plan`

## Current MVP Data Sources

ReturnShield currently uses local JSON files that mirror Shopify concepts:

| MVP File | Shopify Concept |
| --- | --- |
| `backend/app/data/products.json` | Products and variants |
| `backend/app/data/orders.json` | Orders and fulfillment status |
| `backend/app/data/customers.json` | Customers and return history |
| `backend/app/data/policies.json` | Store policies |
| `backend/app/data/tickets.json` | Support or return cases |
| `backend/app/data/conversations.json` | Support conversation history |

## API Mapping

| ReturnShield API | Future Shopify Source |
| --- | --- |
| `GET /api/products/{product_id}` | Shopify Admin Product / ProductVariant APIs |
| `GET /api/orders/{order_id}` | Shopify Admin Order API |
| `POST /api/returns/check` | Shopify order + product + customer history + custom return rules |
| `POST /api/risk-score` | Shopify customer order history + custom risk engine |
| `GET /api/tickets` | Helpdesk integration or custom merchant support store |
| `POST /api/conversations` | Helpdesk conversation thread |
| `POST /api/conversations/{id}/evidence` | File upload + support ticket attachment |

## Suggested Admin API Scopes

For a real custom app, likely scopes would include:

- `read_products`
- `read_orders`
- `read_customers`
- `read_fulfillments`
- `write_returns` or return-related scopes where available
- `write_refunds` only if the app is allowed to initiate refunds

For the MVP, refund initiation should remain simulated. The decision engine can recommend a refund, exchange, replacement, store credit, or human review without actually changing merchant money movement.

## Admin GraphQL Authentication

Shopify Admin GraphQL requests are sent to:

```text
https://{store_name}.myshopify.com/admin/api/2026-04/graphql.json
```

All direct Admin GraphQL requests require:

```text
X-Shopify-Access-Token: {access_token}
```

For this MVP, the optional Shopify adapter reads:

```text
SHOPIFY_STORE_NAME
SHOPIFY_ACCESS_TOKEN
SHOPIFY_API_VERSION
```

If those variables are missing, the adapter falls back to synthetic Shopify-style data so the demo keeps working.

Example query used by the adapter:

```graphql
query ReturnShieldProducts($first: Int!) {
  products(first: $first) {
    edges {
      node {
        id
        title
        productType
        totalInventory
      }
    }
  }
}
```

Demo endpoints:

```http
GET /api/shopify/shop
GET /api/shopify/products
```

## Integration Strategy

The backend is already structured so mock services can later be replaced with Shopify service adapters.

Current:

```text
API route -> local service -> JSON data
```

Now supported for demo:

```text
API route -> Shopify adapter -> Shopify Admin GraphQL API
              |
              +-> synthetic fallback if credentials are missing
```

Future production:

```text
API route -> Shopify adapter -> Shopify Admin API
```

Recommended adapter files:

```text
backend/app/integrations/shopify_client.py
backend/app/integrations/shopify_products.py
backend/app/integrations/shopify_orders.py
backend/app/integrations/shopify_customers.py
```

The return decision engine should stay independent from Shopify. Shopify should provide facts; ReturnShield should make the policy-aware decision.

## Demo Positioning

Use this phrasing in the presentation:

```text
This MVP uses synthetic Shopify-style data, which is allowed by the challenge. The product and engineering focus is the AI support workflow, return eligibility engine, abuse-risk scoring, merchant visibility, and human handoff. The data layer is intentionally isolated so the JSON services can later be swapped with Shopify Admin API adapters.
```
