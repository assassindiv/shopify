# ReturnShield Decision Log

This file records major product and technical decisions made during the MVP build.

## Decision 1: Build ReturnShield As More Than A Chatbot

Decision:

ReturnShield should be an AI support agent plus a deterministic return decision engine.

Reason:

Generic chatbots can answer FAQs, but return/refund decisions require order data, policy rules, customer history, and fraud-risk reasoning.

Tradeoff:

This adds backend complexity, but makes the project more original and business-relevant.

## Decision 2: Use Synthetic Shopify-Style Data For MVP

Decision:

Use local JSON files for products, orders, customers, policies, tickets, and conversations.

Reason:

The challenge allows synthetic data. This keeps the demo reliable and lets the team focus on product workflow and engineering quality.

Tradeoff:

The MVP does not prove full real-store integration, but it includes a Shopify Admin GraphQL adapter path for future integration.

## Decision 3: Keep Risk Scoring Deterministic

Decision:

The LLM does not decide risk score or eligibility. Backend rules calculate them.

Reason:

Refund decisions need consistency, explainability, and merchant trust.

Tradeoff:

Rules are less flexible than a learned fraud model, but they are easier to audit and demo.

## Decision 4: Use Groq For The AI Layer

Decision:

Use Groq's OpenAI-compatible chat API for intent classification, field extraction, and natural language response generation.

Reason:

Groq provides fast LLM responses and is simple to integrate through an OpenAI-compatible endpoint.

Tradeoff:

The app depends on `GROQ_API_KEY` for live AI behavior. The deterministic return APIs still work without Groq.

## Decision 5: Use A Two-Step AI Workflow

Decision:

Use the LLM twice:

1. Parse message and classify intent.
2. Generate final response from backend tool results.

Reason:

This separates understanding from decision-making. The LLM handles language; backend services handle facts and business logic.

Tradeoff:

This uses more LLM calls, but the flow is cleaner and easier to debug.

## Decision 6: Build Customer And Merchant Surfaces Separately

Decision:

Create separate customer and merchant pages:

- `frontend/customer.html`
- `frontend/merchant.html`

Reason:

The product has two different users: customers need simple support, while merchants need tickets, risk signals, and conversations.

Tradeoff:

Two pages require more wiring, but they make the demo clearer and closer to a real support system.

## Decision 7: Add Conversation Sessions

Decision:

Every customer chat gets a `conversationId`, and the merchant console can view the full conversation.

Reason:

A real support system needs durable conversation history and human handoff.

Tradeoff:

Session handling adds state, but prevents the product from feeling like a one-off chatbot.

## Decision 8: Support Merchant Replies

Decision:

Merchants can reply to customer conversations from the merchant console.

Reason:

Human escalation is part of the core product promise.

Tradeoff:

The MVP uses polling instead of real-time WebSockets, but the workflow is functional.

## Decision 9: Simulate Evidence Upload

Decision:

Customer can submit photo proof as a simulated evidence action.

Reason:

Damaged-item claims are central to the suspicious refund demo. Evidence submission makes the flow feel real without needing file storage.

Tradeoff:

There is no actual file upload or image storage yet.

## Decision 10: Add Ticket Lifecycle States

Decision:

Tickets support statuses such as:

- Open
- Evidence Required
- Human Review
- Approved
- Resolved

Reason:

Merchant support teams need a workflow, not just static risk labels.

Tradeoff:

Lifecycle handling is simple for MVP and does not yet include assignment, SLA, or internal notes.

## Decision 11: Add Shopify Admin GraphQL Adapter With Fallback

Decision:

Add `/api/shopify/shop` and `/api/shopify/products` endpoints that call Shopify Admin GraphQL when credentials exist and synthetic data otherwise.

Reason:

This aligns the project with Shopify while keeping the demo stable without real store credentials.

Tradeoff:

Only shop and product reads are implemented for now. Orders, customers, and returns still use synthetic data.

## Decision 12: Use Static HTML For Frontend MVP

Decision:

Use static HTML/CSS/JavaScript instead of setting up React/Vite.

Reason:

It kept development fast and avoided setup overhead during MVP building.

Tradeoff:

Static HTML is less scalable. If the project grows, migrating to React/Vite would be better.

## Decision 13: Store MVP Data In JSON Files

Decision:

Use JSON files for persistence during demo.

Reason:

Simple, inspectable, and enough for a hackathon MVP.

Tradeoff:

JSON files are not safe for concurrent production writes. A database is needed for production.

## Decision 14: Use Polling Instead Of WebSockets

Decision:

Customer and merchant pages poll for updates.

Reason:

Polling is easier to implement and reliable enough for MVP.

Tradeoff:

WebSockets would provide better real-time behavior in production.

## Decision 15: Keep Refund Execution Simulated

Decision:

ReturnShield recommends refund, replacement, exchange, store credit, or review, but does not execute actual refunds.

Reason:

Money movement should require stronger auth, permissions, audit logs, and merchant approval.

Tradeoff:

The MVP demonstrates decision support rather than complete refund automation.
