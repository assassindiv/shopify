# ReturnShield Architecture

ReturnShield has two product surfaces: a customer-facing support chat and a merchant-facing dashboard. Both use the same backend decision engine so the customer response and merchant ticket context stay consistent.

## MVP Architecture

```text
Customer Chat UI                 Merchant Dashboard
       |                                  |
       |                                  |
       +----------- Frontend API Client --+
                          |
                          v
                   FastAPI Backend
                          |
       +------------------+------------------+
       |                  |                  |
       v                  v                  v
 Mock Store Data   Decision Services   Ticket Store
```

## Backend Modules

```text
backend/app
  api/
    health.py
    products.py
    orders.py
    returns.py
    risk.py
    tickets.py
  core/
    config.py
  data/
    products.json
    orders.json
    customers.json
    tickets.json
  models/
    product.py
    order.py
    customer.py
    return_request.py
    ticket.py
  services/
    catalog_service.py
    order_service.py
    return_service.py
    risk_service.py
    ticket_service.py
```

## Frontend Modules

```text
frontend/src
  components/
    ChatPanel
    DashboardMetrics
    TicketQueue
    RiskBadge
  pages/
    ChatDemo
    Dashboard
  lib/
    apiClient
```

## Decision Flow

```text
Customer asks for refund
        |
        v
Collect order ID and reason
        |
        v
Order lookup
        |
        v
Product and customer lookup
        |
        v
Return eligibility check
        |
        v
Risk score calculation
        |
        v
Recommended action
        |
        +--> Customer-facing response
        |
        +--> Ticket creation when evidence or human review is needed
```

## AI Agent Workflow

The customer chat is handled as an AI agent pipeline, not as a fixed template bot.

```text
Customer message
        |
        v
Groq LLM parses message + recent chat history
        |
        v
Intent classification
  - order_tracking
  - product_question
  - policy_question
  - return_request
  - refund_request
  - exchange_request
  - unknown
        |
        v
Field extraction
  - order ID
  - customer email
  - return reason
  - proof availability
        |
        v
Backend tools run deterministic checks
  - order lookup
  - product lookup
  - policy context
  - return eligibility
  - risk scoring
  - ticket creation
        |
        v
Groq LLM writes the customer response using tool results
        |
        v
Conversation is logged for merchant Live Chat
```

The rule-based engine remains the source of truth for eligibility, risk score, and ticket creation. The LLM is responsible for understanding natural language and composing the final response.

## Risk Scoring Inputs

- Customer return frequency.
- Previous refund or damaged-item claims.
- Product price.
- Product category risk.
- Return window timing.
- Photo proof availability.
- Return reason.

## First Demo Path

The first complete path should be the suspicious refund scenario:

```text
Damaged item claim -> ORD-1045 -> high risk -> request photo proof -> create ticket
```
