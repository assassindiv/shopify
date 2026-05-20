# ReturnShield User Stories

## Customer Chat

### Story 1: Ask About Order Status

As a customer, I want to ask where my order is so that I can get an immediate delivery update.

Acceptance criteria:

- Customer can provide an order ID.
- System returns order status.
- If the order does not exist, the system explains that it cannot find the order.

### Story 2: Request A Return Or Refund

As a customer, I want to request a return, refund, or exchange so that I can resolve an issue with my purchase.

Acceptance criteria:

- System detects return/refund/exchange intent.
- System asks for order ID if it is missing.
- System checks order, product, customer, and policy rules.
- System returns a clear decision or next step.

### Story 3: Damaged Item Claim

As a customer, I want to report that an item arrived damaged so that I can receive a replacement, refund, or store credit.

Acceptance criteria:

- System classifies the reason as `damaged_item`.
- System checks whether proof was provided.
- System requests photo proof when risk is medium or high.
- System creates a ticket when human review may be needed.

## Merchant Dashboard

### Story 4: View Return Tickets

As a merchant, I want to see return-related tickets so that I can review risky or sensitive cases.

Acceptance criteria:

- Dashboard shows ticket ID, customer, issue, risk level, and suggested action.
- Tickets created by the return flow appear in the queue.
- High-risk tickets are visually distinguishable.

### Story 5: Understand Risk Reasons

As a merchant, I want to see why a return request was flagged so that I can make a fair decision.

Acceptance criteria:

- Each ticket includes risk score.
- Each ticket includes risk reasons.
- Reasons are human-readable.

### Story 6: Track Business Impact

As a merchant, I want overview metrics so that I can understand how ReturnShield is helping my store.

Acceptance criteria:

- Dashboard shows total support chats.
- Dashboard shows AI-resolved tickets.
- Dashboard shows human escalations.
- Dashboard shows refunds prevented.
- Dashboard shows exchanges suggested.

## Support Agent

### Story 7: Review High-Risk Case

As a support agent, I want high-risk cases escalated with context so that I do not need to manually reconstruct the customer history.

Acceptance criteria:

- High-risk return requests create tickets.
- Ticket contains order, customer, product, return reason, risk score, and suggested action.
- Ticket includes enough context to continue the support workflow.
