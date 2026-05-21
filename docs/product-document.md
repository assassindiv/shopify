# ReturnShield Product Document

## Product Name

ReturnShield: Shopify AI Support Agent with Return Abuse Detection

## Product Summary

ReturnShield is a Shopify-native AI customer support system that helps customers with product questions, policy questions, order tracking, returns, refunds, and exchanges. Its differentiator is a return decision engine that checks eligibility, customer history, product rules, and risk signals before recommending refund, exchange, replacement, store credit, or human review.

## Target Users

- Customers who need fast support for orders, products, policies, returns, refunds, and exchanges.
- Shopify merchants who want to reduce repetitive support workload and prevent unnecessary refund losses.
- Merchant support agents who need context, risk reasons, and recommended actions before reviewing return cases.

## Problem

Most support chatbots can answer simple questions, but returns and refunds require actual business judgment. A merchant needs to know:

- Is the order valid?
- Was the product delivered?
- Is the item still within the return window?
- Is the product returnable?
- Has this customer requested many returns recently?
- Is the claim suspicious or high-value?
- Should the system approve, ask for evidence, or escalate?

ReturnShield solves this by combining AI chat with deterministic return rules and risk scoring.

## Core Features

### Customer Support Chat

Customers can ask:

- Where is my order?
- Is this product available in size M?
- What is your return policy?
- I want to return this item.
- My product arrived damaged.
- Can I exchange this instead of refunding?

The chat uses Groq to classify intent, extract details, and generate natural responses grounded in backend tool results.

### Product Q&A

The agent answers from synthetic Shopify-style catalog data. If a requested product or product detail is missing, it should say it does not have enough catalog information instead of inventing an answer.

### Policy Q&A

The agent answers from mock policy documents stored in `backend/app/data/policies.json`.

### Order Tracking

The agent checks mock order data for status, carrier, tracking ID, expected delivery, and timeline.

### Return Decision Engine

For return/refund/exchange requests, ReturnShield:

1. Verifies order and customer email.
2. Checks delivery status.
3. Checks return window.
4. Checks product returnability.
5. Classifies return reason.
6. Checks customer return history.
7. Calculates risk score.
8. Recommends action.
9. Creates or updates support ticket.
10. Logs the conversation for merchant review.

### Return Abuse Detection

Risk signals include:

- More than 3 returns in the last 60 days.
- High-value item above INR 5000.
- Damaged-item claim without proof.
- Repeated damage or refund claims.
- High-risk product category.
- Return request near the deadline.

Risk levels:

| Score | Risk Level | Action |
| ---: | --- | --- |
| 0-30 | Low | Auto-approve |
| 31-60 | Medium | Ask for evidence |
| 61+ | High | Human review |

### Merchant Console

The merchant console shows:

- Dashboard metrics.
- Ticket queue.
- Risk levels.
- Customer conversations.
- Merchant replies.
- Evidence submission state.
- Ticket approve/resolve actions.

## Main Demo Scenario

Customer:

```text
I want a refund. The shoes arrived damaged.
```

Customer provides:

```text
ORD-1045, aarav@example.com
```

System result:

- Order is delivered.
- Return window is open.
- Product is returnable.
- Customer has 4 recent returns.
- Customer has previous damage claims.
- No photo proof is present.
- Risk score is high.
- Ticket `T-104` appears in merchant console.
- Merchant can reply.
- Customer can submit proof.

## Current MVP Scope

Built:

- AI chat with Groq.
- Synthetic Shopify-style data.
- Return eligibility engine.
- Risk scoring.
- Merchant dashboard.
- Customer conversation logging.
- Merchant replies.
- Evidence submission.
- Optional Shopify Admin GraphQL adapter with synthetic fallback.

Out of scope for MVP:

- Real refund processing.
- Real Shopify OAuth install flow.
- Real authentication.
- Production database.
- Real file storage.
- Vector search over uploaded policy documents.

## Business Value

ReturnShield helps merchants:

- Reduce support workload.
- Identify suspicious refund behavior.
- Prevent unnecessary refund losses.
- Convert refunds into exchanges when appropriate.
- Give support agents clear context before escalation.
- Improve customer response time.
