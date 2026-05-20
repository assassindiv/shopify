# ReturnShield Sprint Plan

## Delivery Method

Use short Agile increments where each sprint produces a working, demoable slice. The MVP should prioritize the suspicious refund scenario first, because it proves the unique value of ReturnShield.

## Two-Person Ownership Strategy

The team will use a customer-side vs merchant-side split. Both people use `docs/api-contract.md` as the shared contract.

### Person 1: Customer Side

Owns the customer-facing support experience.

Responsibilities:

- Customer chat flow.
- Order tracking experience.
- Return/refund/exchange conversation.
- Return reason capture.
- Customer-facing response text.
- API calls needed by the customer UI.
- Demo path from customer message to return decision.

Primary files:

- `frontend/src/pages/ChatDemo`
- `frontend/src/components/ChatPanel`
- `frontend/src/lib/apiClient`
- Customer-related backend routes if needed during integration.

### Person 2: Merchant Side

Owns the merchant-facing dashboard and review workflow.

Responsibilities:

- Merchant dashboard layout.
- Overview metrics.
- Ticket queue.
- Risk badges.
- Return analytics summary.
- Policy manager mock UI.
- Dashboard connection to tickets and return-risk APIs.

Primary files:

- `frontend/src/pages/Dashboard`
- `frontend/src/components/DashboardMetrics`
- `frontend/src/components/TicketQueue`
- `frontend/src/components/RiskBadge`
- Dashboard-related backend routes if needed during integration.

### Shared Backend Contract

Both people coordinate on:

- `POST /api/returns/check`
- `GET /api/tickets`
- shared mock IDs such as `ORD-1045`, `CUS-501`, `PROD-201`, and `T-104`
- final demo script
- README setup instructions

## Sprint 0: Project Foundation

Goal: Create the project structure and source-of-truth documentation.

Tasks:

- Create backend, frontend, and docs folders.
- Write product requirements.
- Write user stories.
- Define MVP API contract.
- Document system architecture.

Done when:

- Repository has a clear structure.
- MVP scope is documented.
- Engineering work can start without guessing the product behavior.

## Sprint 1: Backend Decision Engine

Goal: Build the core business logic that powers the demo.

Tasks:

- Set up FastAPI backend.
- Add mock product, order, customer, policy, and ticket data.
- Implement order lookup service.
- Implement product lookup service.
- Implement return reason classification constants.
- Implement risk scoring service.
- Implement return eligibility service.
- Implement ticket creation service.
- Add API routes for health, products, orders, returns, risk score, and tickets.

Done when:

- `ORD-1045` suspicious refund scenario returns a high-risk decision.
- Risk score includes human-readable reasons.
- Return check can create a ticket.
- Backend can run locally.

Owner:

- Customer-side person leads return check behavior.
- Merchant-side person reviews ticket output shape for dashboard needs.

## Sprint 2: Merchant Dashboard

Goal: Show business value to the merchant.

Tasks:

- Set up frontend app.
- Build dashboard layout.
- Build overview metric cards.
- Build ticket queue.
- Build return analytics summary.
- Connect dashboard to backend APIs.

Done when:

- Merchant can see tickets and risk levels.
- High-risk cases are easy to identify.
- Dashboard reflects the suspicious refund demo output.

Owner:

- Merchant-side person leads.
- Customer-side person verifies the dashboard reflects chat-created cases.

## Sprint 3: Customer Chat Demo

Goal: Make the core flow feel like an AI support product.

Tasks:

- Build customer chat UI.
- Add scripted chat flow for return/refund requests.
- Ask for missing order number.
- Call return check API.
- Render customer-facing response.
- Show next actions such as upload proof, replacement, store credit, or escalation.

Done when:

- User can run the full suspicious refund scenario from chat.
- Dashboard updates with the resulting ticket.

Owner:

- Customer-side person leads.
- Merchant-side person verifies the created ticket is readable and useful.

## Sprint 4: Polish And Demo Readiness

Goal: Make the product coherent, reliable, and presentable.

Tasks:

- Improve UI states.
- Add loading and error states.
- Add empty states.
- Add seed demo data.
- Review README for setup instructions.
- Add final demo script.

Done when:

- Project can be cloned and run from documented commands.
- Demo scenario works end to end.
- README explains the product, setup, and demo flow.
