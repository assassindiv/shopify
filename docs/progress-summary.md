# ReturnShield Progress Summary

## What We Built

ReturnShield is now an MVP customer-merchant support system for Shopify-style stores. It combines a Groq-powered AI customer chat with a deterministic return decision engine and a merchant console.

## Current Workflow

```text
Customer message
        |
        v
Groq LLM parses message and conversation history
        |
        v
Intent classification and field extraction
        |
        v
Backend tools run deterministic checks
        |
        v
Groq generates the customer-facing response
        |
        v
Conversation and ticket appear in merchant console
```

## Backend Completed

- FastAPI app structure.
- Groq AI chat endpoint.
- Intent classification through Groq.
- Field extraction for order ID, email, return reason, and proof availability.
- Product lookup from mock catalog.
- Policy grounding from mock policy documents.
- Order tracking from mock order database.
- Return eligibility engine.
- Risk scoring engine.
- Ticket creation.
- Ticket lifecycle updates.
- Evidence submission.
- Conversation sessions.
- Merchant replies.
- Dashboard metrics API.
- CORS support for local frontend development.
- Local `.env` support for `GROQ_API_KEY`.

## Frontend Completed

- `frontend/customer.html`
  - customer support chat
  - Groq-backed AI responses
  - conversation session storage
  - typing indicator
  - suspicious refund demo
  - order tracking demo
  - policy question demo
  - photo proof submission
  - polling for merchant replies

- `frontend/merchant.html`
  - merchant dashboard
  - live metrics from backend
  - live ticket queue
  - risk badges
  - approve/resolve actions
  - live customer conversation list
  - merchant reply support

## Key APIs

```text
POST /api/chat
GET /api/conversations
POST /api/conversations
GET /api/conversations/{conversation_id}
POST /api/conversations/{conversation_id}/messages
POST /api/conversations/{conversation_id}/evidence
GET /api/tickets
PATCH /api/tickets/{ticket_id}
GET /api/dashboard/overview
GET /api/orders/{order_id}
GET /api/products/{product_id}
POST /api/returns/check
POST /api/risk-score
```

## Demo Scenario

Customer:

```text
I want a refund. The shoes arrived damaged.
```

Then:

```text
ORD-1045, aarav@example.com
```

System result:

- Order is delivered.
- Return window is still open.
- Product is returnable.
- Customer has multiple recent returns.
- Customer has previous damage claims.
- No photo proof provided.
- Risk score is high.
- Ticket `T-104` is created or updated.
- Merchant sees the conversation and ticket.
- Customer can submit proof.
- Merchant can reply or resolve the case.

## Core Modules Status

| Module | Status |
| --- | --- |
| Customer support chat | Built |
| Product Q&A from catalog | Built for mock catalog |
| Missing product data handling | Built |
| Policy Q&A from policy docs | Built with mock policy JSON |
| Order tracking | Built with mock order data |
| Return/refund/exchange flow | Built |
| Risk scoring | Built |
| Merchant dashboard | Built |
| Merchant replies | Built |
| Evidence submission | Built |
| Ticket lifecycle | Built |

## Current Limitations

- Policy upload is simulated with `backend/app/data/policies.json`; there is no real upload UI yet.
- Catalog and order data are mock JSON files.
- There is no real Shopify API integration.
- There is no real authentication.
- There is no production database.
- Customer/merchant live updates use polling, not WebSockets.
- There are not yet automated tests.

## Suggested Next Steps

1. Add backend tests for risk scoring, return checks, conversations, and ticket updates.
2. Add a polished root README with setup and demo instructions.
3. Add more mock products, orders, and policies.
4. Add policy upload/edit API for the merchant console.
5. Add simple auth-role simulation.
6. Convert static HTML frontend into React/Vite if more scale is needed.
