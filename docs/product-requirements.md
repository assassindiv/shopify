# ReturnShield Product Requirements

## Product Summary

ReturnShield is a Shopify-native AI support agent that combines customer support automation with refund-loss prevention. It answers product, policy, and order questions, but its key strength is handling returns through a structured decision engine that evaluates eligibility, customer history, product rules, and risk signals before recommending refund, exchange, replacement, store credit, or human review.

## Problem

Shopify merchants lose time and money handling repetitive customer support and return requests. Standard chatbots can answer simple questions, but they usually fail when the request requires business judgment: checking orders, interpreting policies, reviewing customer history, and deciding whether a refund should be approved.

ReturnShield solves this by acting as both a customer support assistant and a return decision engine.

## Target Users

- Customers who need quick answers about products, orders, policies, returns, refunds, or exchanges.
- Shopify merchants who want to reduce support workload and prevent unnecessary refund losses.
- Human support agents who need risk context and recommended actions before reviewing sensitive cases.

## MVP Goal

Build an end-to-end demo where a customer requests a suspicious refund, the system checks mock Shopify data, calculates return risk, gives a policy-aware response, and creates a dashboard-visible ticket.

## MVP Scope

### Customer Chat

- Accept customer messages.
- Detect return/refund/exchange intent.
- Ask for missing order number when needed.
- Return a clear customer-facing response.

### Order Tracking

- Look up mock orders by order ID.
- Return current order status and delivery information.

### Return Decision Engine

- Verify order exists.
- Check order status.
- Check delivery date and return window.
- Check product category and returnability.
- Classify return reason.
- Check customer return history.
- Calculate risk score.
- Recommend action.
- Create a support ticket when review or evidence is required.

### Risk Scoring

Risk signals:

- More than 3 returns in last 60 days.
- Item value above INR 5000.
- Damaged-item claim without photo proof.
- Return requested on final return-window day.
- Repeated refund or damage claims.
- High-risk product category.

Risk levels:

| Score | Risk Level | Action |
| ---: | --- | --- |
| 0-30 | Low | Auto-approve |
| 31-60 | Medium | Ask for more evidence |
| 61+ | High | Human review |

### Merchant Dashboard

- Show overview metrics.
- Show ticket queue.
- Show risk level and suggested action for each return case.
- Show reasons behind risk scoring.

## Out Of Scope For MVP

- Real Shopify API integration.
- Real payment or refund processing.
- Real file uploads for policy documents or photo proof.
- Real authentication.
- Production database.
- Full RAG over uploaded policy documents.
- Machine learning fraud model.
- WhatsApp, voice, or multilingual support.

## Primary Demo Scenario

Customer:

```text
I want a refund. The shoes arrived damaged.
```

Agent asks for order number.

Customer:

```text
ORD-1045
```

System checks:

- Order delivered 6 days ago.
- Return window is 7 days.
- Product is returnable.
- Customer has returned 4 items in last 45 days.
- Customer has 2 previous damaged-item claims.
- No photo proof was provided.

Customer response:

```text
I can help with this. Since the item is within the return window, your request is eligible for review. Because this account has multiple recent damage-related refund claims, I need a photo of the damaged product before approving a refund. Once uploaded, I can offer a replacement, store credit, or escalate this to our support team.
```

Dashboard result:

```text
Risk level: High
Reason: 4 returns in 45 days + repeated damage claims + no evidence
Suggested action: Request photo proof and escalate if unclear
```

## Success Metrics

- Customer can complete the suspicious refund demo flow without developer intervention.
- Return decision output includes eligibility, risk score, risk reasons, and suggested action.
- Dashboard reflects the created ticket and risk classification.
- Product feels more advanced than a generic support chatbot because the decision engine is visible and explainable.

## Future Enhancements

- Real Shopify API integration.
- Policy document upload and retrieval.
- Photo/video proof upload.
- Automated return label generation.
- Courier tracking integration.
- ML-based fraud detection.
- Multilingual support.
- WhatsApp integration.
- Customer sentiment detection.
- Product return-rate recommendations.
