# ReturnShield Contribution Document

## Contributors

- Divyanshu Puri
- Eshan Saxena

## Collaboration Strategy

The project was divided using a customer-side and merchant-side ownership model.

### Customer Side

Focus:

- Customer support chat.
- Groq AI conversation flow.
- Intent classification and extraction.
- Return/refund/exchange customer experience.
- Evidence submission.
- Order tracking and policy/product Q&A experience.

Main areas:

- `frontend/customer.html`
- `backend/app/api/chat.py`
- `backend/app/services/chat_service.py`
- `backend/app/services/return_service.py`
- `backend/app/services/risk_service.py`

### Merchant Side

Focus:

- Merchant dashboard.
- Ticket queue.
- Risk badges and metrics.
- Customer conversation visibility.
- Merchant replies.
- Ticket lifecycle actions.

Main areas:

- `frontend/merchant.html`
- `backend/app/api/dashboard.py`
- `backend/app/api/tickets.py`
- `backend/app/api/conversations.py`
- `backend/app/services/dashboard_service.py`
- `backend/app/services/ticket_service.py`
- `backend/app/services/conversation_service.py`

## Shared Work

Shared responsibilities:

- Product idea and positioning.
- Return abuse detection logic.
- Synthetic Shopify-style data design.
- Demo scenario.
- Documentation.
- API contract.
- Shopify integration readiness.

## Development Notes

The team prioritized a working end-to-end MVP:

```text
Customer asks for refund
        |
        v
AI classifies intent
        |
        v
Decision engine calculates risk
        |
        v
Customer receives response
        |
        v
Merchant sees ticket and conversation
        |
        v
Merchant can reply or update ticket
```

## Contribution Summary

Major completed areas:

- Product requirements and sprint planning.
- FastAPI backend.
- Groq AI chat integration.
- Return eligibility logic.
- Risk scoring engine.
- Customer chat UI.
- Merchant dashboard UI.
- Conversation logging.
- Merchant reply workflow.
- Evidence submission.
- Shopify Admin GraphQL adapter with synthetic fallback.
- Technical and product documentation.

## Suggested Future Contributions

- Add backend automated tests.
- Replace JSON storage with a database.
- Add authentication and role-based access.
- Add real file upload for evidence.
- Add policy upload and document retrieval.
- Add WebSocket-based live chat.
- Connect real Shopify development store data.
