# ReturnShield

## Shopify AI Support Agent with Return Abuse Detection

ReturnShield is a Shopify-native AI customer support agent that helps merchants automate customer service while reducing refund losses. It handles product questions, policy queries, order tracking, return/refund requests, and human escalation.

Unlike a generic chatbot, ReturnShield works like a **policy-aware decision engine**. It verifies orders, checks return eligibility, analyzes customer return history, calculates risk, and recommends the best resolution: refund, exchange, replacement, partial refund, store credit, or human review.

---

## Problem Statement

E-commerce merchants receive many repetitive support requests every day:

- "Where is my order?"
- "Can I return this item?"
- "I received a damaged product."
- "Can I get a refund?"
- "Is this product available in my size?"

Most AI support tools can answer simple questions, but they often fail when real business decisions are involved. Refunds and returns require checking order data, customer history, product rules, policy conditions, and fraud risk.

ReturnShield solves this by combining AI customer support with a structured return decision engine.

---

## Key Features

### 1. Product Q&A

Customers can ask questions about products, availability, sizes, materials, warranty, and features.

The agent answers using store catalog data and avoids hallucination when product details are missing.

Example:

```text
Customer: Is this backpack waterproof?

Agent: This backpack is water-resistant, not fully waterproof. It can handle light rain, but it is not designed for heavy rain or submersion.
```

### 2. Policy Q&A

Merchants can upload policy documents such as:

- Return policy
- Refund policy
- Shipping policy
- Warranty policy
- Exchange rules

The agent uses these documents to answer policy-related questions.

Example:

```text
Customer: Can I return a sale item?

Agent: According to the store policy, sale items are not eligible for refunds unless they arrive damaged or the wrong item was delivered.
```

### 3. Order Tracking

ReturnShield can check a mock order database and provide real-time order updates.

Supported order statuses include:

- Processing
- Packed
- Shipped
- Out for delivery
- Delivered
- Delayed
- Failed delivery
- Returned to sender

Example:

```text
Customer: Where is my order ORD-1042?

Agent: Your order has been shipped and is currently out for delivery. Expected delivery is today by 8 PM.
```

### 4. Return and Refund Decision Engine

When a customer requests a return, refund, or exchange, the agent follows a structured decision flow.

Flow:

1. Verify order number and customer email
2. Check order status
3. Check delivery date
4. Check return window
5. Check product category rules
6. Check whether the item is returnable
7. Classify the return reason
8. Check customer return history
9. Calculate return-risk score
10. Recommend the best resolution
11. Explain the decision using policy rules
12. Escalate to a human if needed

### 5. Return Abuse Detection

ReturnShield protects merchants by identifying suspicious return behavior.

It checks risk signals such as:

- Too many previous returns
- Multiple recent refund claims
- Repeated damaged-item claims
- High-value item return
- Missing photo or video proof
- Return requested near the deadline
- Non-returnable product category
- Unusual customer behavior

Example scoring logic:

| Condition | Risk Points |
| --- | ---: |
| More than 3 returns in 60 days | +20 |
| Product value above INR 5000 | +20 |
| Damage claim without photo proof | +15 |
| Return requested on final return-window day | +15 |
| Repeated refund claims | +20 |
| High-risk product category | +10 |

Risk classification:

| Score | Risk Level | Action |
| --- | --- | --- |
| 0-30 | Low Risk | Auto-approve |
| 31-60 | Medium Risk | Ask for evidence |
| 61+ | High Risk | Human review |

### 6. Human Escalation

Some cases should not be handled automatically.

ReturnShield escalates when:

- Risk score is high
- Policy conflict exists
- Customer asks for a special exception
- Order data is incomplete
- Item is high-value
- Customer is angry or dissatisfied
- The agent is uncertain

### 7. Merchant Dashboard

The admin dashboard helps merchants monitor support activity and return patterns.

Dashboard sections:

#### Overview

- Total support chats
- AI-resolved tickets
- Human escalations
- Refunds prevented
- Exchanges suggested
- Average response time

#### Return Analytics

- Most returned products
- Common return reasons
- High-risk customers
- Refund amount saved
- Exchange conversion rate

#### Ticket Queue

| Ticket ID | Issue | Risk Level | Suggested Action |
| --- | --- | --- | --- |
| T-101 | Size issue | Low | Exchange |
| T-102 | Damaged item | Medium | Ask for photo proof |
| T-103 | Repeated refunds | High | Human review |

#### Policy Manager

Merchants can upload or edit:

- Return rules
- Refund rules
- Category restrictions
- Warranty terms
- Escalation rules

---

## Example Demo Flow

### Scenario: Suspicious Refund Request

```text
Customer: I want a refund. The shoes arrived damaged.

Agent: I can help with that. Please share your order number.

Customer: ORD-1045
```

System checks:

- Order Status: Delivered
- Delivered: 6 days ago
- Return Window: 7 days
- Product Category: Footwear
- Product Returnable: Yes
- Customer Returns: 4 returns in last 45 days
- Previous Claims: 2 damaged-item claims
- Photo Proof: Not provided

Agent response:

```text
Your order is still within the return window, so I can help you with this request.

Since this account has multiple recent damage-related refund claims, I will need a photo of the damaged product before approving a refund.

After verification, I can offer a replacement, store credit, or escalate this to a support specialist.
```

Dashboard output:

- Risk Level: High
- Reason: Multiple recent returns + repeated damage claims + no proof
- Suggested Action: Request photo proof and escalate if unclear

---

## Tech Stack

Suggested stack:

### Frontend

- React.js / Next.js
- Tailwind CSS
- Shadcn UI
- Recharts for analytics charts

### Backend

- FastAPI
- Python REST APIs for order, catalog, policy, risk, return, and ticket data
- Pydantic models for request and response validation
- Mock Shopify data integration

### Database

- MongoDB / PostgreSQL
- Stores products, orders, customers, policies, tickets, and return history

### AI Layer

- LLM for natural language understanding and response generation
- Retrieval-Augmented Generation for policy Q&A
- Tool-calling for order lookup, product search, return eligibility, and ticket creation

### Optional

- Vector database for policy search
- Admin authentication
- File upload for policy documents

---

## System Architecture

```text
Customer Chat Widget
        |
        v
AI Support Agent
        |
        |---------------- Product Catalog Tool
        |---------------- Policy Retrieval Tool
        |---------------- Order Lookup Tool
        |---------------- Return Eligibility Tool
        |---------------- Risk Scoring Engine
        |---------------- Ticket Creation Tool
        |
        v
Merchant Dashboard
```

---

## Core API Examples

### Get Product Details

```http
GET /api/products/{product_id}
```

### Track Order

```http
GET /api/orders/{order_id}
```

### Check Return Eligibility

```http
POST /api/returns/check
```

Example body:

```json
{
  "orderId": "ORD-1045",
  "customerEmail": "customer@example.com",
  "reason": "damaged_item"
}
```

### Calculate Risk Score

```http
POST /api/risk-score
```

Example response:

```json
{
  "riskScore": 75,
  "riskLevel": "High",
  "reasons": [
    "4 returns in last 45 days",
    "Repeated damaged-item claims",
    "No photo proof provided"
  ],
  "recommendedAction": "Request proof and escalate if unclear"
}
```

### Create Support Ticket

```http
POST /api/tickets
```

---

## Data Models

### Product

```json
{
  "id": "PROD-201",
  "name": "Urban Runner Shoes",
  "category": "Footwear",
  "price": 5499,
  "returnable": true,
  "returnWindowDays": 7,
  "stock": 12
}
```

### Order

```json
{
  "id": "ORD-1045",
  "customerId": "CUS-501",
  "productId": "PROD-201",
  "status": "Delivered",
  "deliveredAt": "2025-02-10",
  "amount": 5499
}
```

### Customer

```json
{
  "id": "CUS-501",
  "name": "Aarav Sharma",
  "email": "aarav@example.com",
  "returnsLast60Days": 4,
  "previousDamageClaims": 2
}
```

### Return Request

```json
{
  "id": "RET-301",
  "orderId": "ORD-1045",
  "reason": "damaged_item",
  "riskScore": 75,
  "riskLevel": "High",
  "status": "Evidence Required"
}
```

---

## Return Decision Logic

```text
If order is not delivered:
    Do not allow return yet

If product is non-returnable:
    Reject or escalate if damaged/wrong item

If return window expired:
    Reject or offer human review for exceptions

If reason is size issue:
    Recommend exchange

If reason is damaged item:
    Ask for photo proof
    If low risk, approve replacement/refund
    If high risk, escalate

If customer has repeated refund claims:
    Increase risk score

If risk score is high:
    Human review required
```

---

## Why ReturnShield Is Different

Most support bots only answer questions.

ReturnShield makes structured support decisions by combining:

- Store data
- Policy documents
- Order history
- Customer behavior
- Risk scoring
- Merchant rules
- Human escalation

This makes it useful for real commerce workflows, not just customer conversation.

---

## Business Impact

ReturnShield helps merchants:

- Reduce support workload
- Reduce refund abuse
- Prevent unnecessary refund losses
- Increase exchanges instead of refunds
- Improve customer experience
- Identify products with high return rates
- Understand common customer issues

---

## Judging Criteria Fit

### Product Thinking & Documentation

ReturnShield has clear workflows, edge-case handling, policy reasoning, and risk-based decisions.

### Technical Execution

The system uses tool-calling, mock databases, RAG over policy documents, risk scoring, and dashboard analytics.

### Product Experience

It includes both a customer-facing chat interface and a merchant-facing admin dashboard.

### Business Relevance

It directly reduces support costs and refund losses for Shopify merchants.

### Originality

The return abuse detection and refund-loss prevention layer make it more distinctive than a generic AI support chatbot.

---

## Future Improvements

- Real Shopify API integration
- Automated return label generation
- Courier tracking integration
- Fraud detection using machine learning
- Multi-language support
- Voice support
- WhatsApp integration
- Customer sentiment detection
- Product return-rate recommendations
- Automated policy improvement suggestions
