# ReturnShield Technical Document

## Architecture Overview

ReturnShield has three main layers:

```text
Customer Chat UI        Merchant Console UI
        |                       |
        +----------+------------+
                   |
              FastAPI Backend
                   |
   +---------------+----------------+
   |               |                |
Groq AI Layer  Decision Engine  Synthetic Shopify Data
```

## Tech Stack

Backend:

- Python
- FastAPI
- Pydantic
- httpx
- python-dotenv
- Groq OpenAI-compatible chat API

Frontend:

- Static HTML/CSS/JavaScript for MVP speed.
- `frontend/customer.html`
- `frontend/merchant.html`

Data:

- Local JSON files under `backend/app/data`.
- Optional Shopify Admin GraphQL adapter with synthetic fallback.

## Backend Structure

```text
backend/app
  api/
    chat.py
    conversations.py
    dashboard.py
    health.py
    orders.py
    products.py
    returns.py
    risk.py
    shopify.py
    tickets.py
  core/
    config.py
    errors.py
  data/
    conversations.json
    customers.json
    orders.json
    policies.json
    products.json
    tickets.json
  integrations/
    shopify_client.py
    shopify_products.py
    shopify_shop.py
  models/
  services/
```

## AI Workflow

```text
Customer message
        |
        v
Groq extracts intent, order ID, email, return reason, proof state
        |
        v
Backend tools fetch product/order/customer/policy data
        |
        v
Return decision engine calculates eligibility and risk
        |
        v
Groq generates customer-facing response from tool output
        |
        v
Conversation and ticket are saved for merchant review
```

The LLM does not decide risk score or eligibility. Those are deterministic backend decisions.

## Key Backend APIs

```text
POST /api/chat
GET /api/conversations
POST /api/conversations
GET /api/conversations/{conversation_id}
POST /api/conversations/{conversation_id}/messages
POST /api/conversations/{conversation_id}/evidence
GET /api/dashboard/overview
GET /api/orders/{order_id}
GET /api/products/{product_id}
POST /api/returns/check
POST /api/risk-score
GET /api/tickets
PATCH /api/tickets/{ticket_id}
GET /api/shopify/shop
GET /api/shopify/products
```

## Data Files

| File | Purpose |
| --- | --- |
| `products.json` | Synthetic Shopify products and attributes |
| `orders.json` | Synthetic order, delivery, tracking, and timeline data |
| `customers.json` | Synthetic customer profiles and return history |
| `policies.json` | Mock policy documents |
| `tickets.json` | Support and return cases |
| `conversations.json` | Customer/merchant conversation history |

## Risk Scoring Logic

Risk score is calculated using deterministic rules:

- `+20` if customer has more than 3 returns in 60 days.
- `+20` if item value is above INR 5000.
- `+15` if damaged claim has no photo proof.
- `+15` if return is requested on final return-window day.
- `+20` if customer has repeated refund or damage claims.
- `+10` if product category is high risk.

Risk classification:

- `0-30`: Low
- `31-60`: Medium
- `61+`: High

## Shopify Adapter

The optional Shopify adapter supports:

```text
GET /api/shopify/shop
GET /api/shopify/products
```

If these environment variables are present, it calls Shopify Admin GraphQL:

```text
SHOPIFY_STORE_NAME
SHOPIFY_ACCESS_TOKEN
SHOPIFY_API_VERSION
```

If they are missing, it returns synthetic Shopify-style data so the demo remains reliable.

## Environment Variables

Required for AI:

```text
GROQ_API_KEY
```

Optional:

```text
GROQ_MODEL
SHOPIFY_STORE_NAME
SHOPIFY_ACCESS_TOKEN
SHOPIFY_API_VERSION
```

## Running Locally

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Static frontend:

```bash
python -m http.server 5500
```

Open:

```text
http://localhost:5500/frontend/customer.html
http://localhost:5500/frontend/merchant.html
```

## Current Technical Limitations

- JSON files are used instead of a database.
- Polling is used instead of WebSockets.
- Policy upload is not implemented yet.
- Evidence upload is simulated, not real file storage.
- Authentication is not implemented.
- Automated tests are still recommended.
