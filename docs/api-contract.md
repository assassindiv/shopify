# ReturnShield API Contract

Base path:

```text
/api
```

## Health Check

```http
GET /api/health
```

Response:

```json
{
  "status": "ok",
  "service": "returnshield-api"
}
```

## Shopify Demo Adapter

These endpoints use Shopify Admin GraphQL when credentials are configured, and synthetic Shopify-style data when credentials are missing.

```http
GET /api/shopify/shop
GET /api/shopify/products?first=3
```

Synthetic response example:

```json
{
  "source": "synthetic",
  "shop": {
    "name": "Synthetic ReturnShield Dev Store",
    "myshopifyDomain": "synthetic-dev-store.myshopify.com",
    "apiVersion": "2026-04"
  }
}
```

## AI Chat

Uses Groq to classify customer intent, extract order details, call ReturnShield tools, and write the customer-facing reply.

```http
POST /api/chat
```

Request:

```json
{
  "message": "I want a refund. The shoes arrived damaged. ORD-1045, aarav@example.com",
  "history": []
}
```

Response:

```json
{
  "message": "I can help with this. Since the item is within the return window, your request is eligible for review. Because this account has multiple recent damage-related refund claims, I need a photo of the damaged product before approving a refund.",
  "intent": "refund_request",
  "extraction": {
    "intent": "refund_request",
    "orderId": "ORD-1045",
    "customerEmail": "aarav@example.com",
    "reason": "damaged_item",
    "photoProofProvided": false,
    "needsMoreInfo": false
  },
  "returnDecision": {
    "eligible": true,
    "returnWindowDays": 7,
    "daysSinceDelivery": 6,
    "reason": "damaged_item",
    "riskScore": 75,
    "riskLevel": "High",
    "riskReasons": [
      "Customer has 4 returns in the last 60 days",
      "Item value is above INR 5000",
      "Damage claim has no photo proof",
      "Customer has repeated damaged-item claims"
    ],
    "recommendedAction": "Request photo proof and escalate if unclear",
    "customerMessage": "I can help with this. Since the item is within the return window, your request is eligible for review. Because this account has multiple recent damage-related refund claims, I need a photo of the damaged product before approving a refund. Once uploaded, I can offer a replacement, store credit, or escalate this to our support team.",
    "ticketId": "T-104"
  },
  "aiProvider": "groq",
  "aiModel": "llama-3.1-8b-instant"
}
```

## Get Product

```http
GET /api/products/{product_id}
```

Response:

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

## Get Order

```http
GET /api/orders/{order_id}
```

Response:

```json
{
  "id": "ORD-1045",
  "customerId": "CUS-501",
  "productId": "PROD-201",
  "status": "Delivered",
  "deliveredAt": "2026-05-14",
  "amount": 5499
}
```

## Check Return

```http
POST /api/returns/check
```

Request:

```json
{
  "orderId": "ORD-1045",
  "customerEmail": "aarav@example.com",
  "reason": "damaged_item",
  "photoProofProvided": false
}
```

Response:

```json
{
  "eligible": true,
  "returnWindowDays": 7,
  "daysSinceDelivery": 6,
  "reason": "damaged_item",
  "riskScore": 75,
  "riskLevel": "High",
  "riskReasons": [
    "Customer has 4 returns in the last 60 days",
    "Item value is above INR 5000",
    "Damage claim has no photo proof",
    "Customer has repeated damaged-item claims"
  ],
  "recommendedAction": "Request photo proof and escalate if unclear",
  "customerMessage": "I can help with this. Since the item is within the return window, your request is eligible for review. Because this account has multiple recent damage-related refund claims, I need a photo of the damaged product before approving a refund. Once uploaded, I can offer a replacement, store credit, or escalate this to our support team.",
  "ticketId": "T-104"
}
```

## Calculate Risk Score

```http
POST /api/risk-score
```

Request:

```json
{
  "orderId": "ORD-1045",
  "reason": "damaged_item",
  "photoProofProvided": false
}
```

Response:

```json
{
  "riskScore": 75,
  "riskLevel": "High",
  "reasons": [
    "Customer has 4 returns in the last 60 days",
    "Item value is above INR 5000",
    "Damage claim has no photo proof",
    "Customer has repeated damaged-item claims"
  ],
  "recommendedAction": "Request photo proof and escalate if unclear"
}
```

## List Tickets

```http
GET /api/tickets
```

Response:

```json
[
  {
    "id": "T-104",
    "customerName": "Aarav Sharma",
    "issue": "Damaged item",
    "riskLevel": "High",
    "riskScore": 75,
    "suggestedAction": "Request photo proof and escalate if unclear",
    "status": "Evidence Required"
  }
]
```

## List Customer Conversations

```http
GET /api/conversations
```

Create a session:

```http
POST /api/conversations
```

Merchant reply:

```http
POST /api/conversations/{conversation_id}/messages
```

Submit customer evidence:

```http
POST /api/conversations/{conversation_id}/evidence
```

Response:

```json
[
  {
    "id": "C-1001",
    "customerEmail": "aarav@example.com",
    "orderId": "ORD-1045",
    "intent": "refund_request",
    "status": "Escalated",
    "riskLevel": "High",
    "ticketId": "T-104",
    "updatedAt": "2026-05-20T12:00:00Z",
    "messages": [
      {
        "role": "customer",
        "content": "I want a refund. The shoes arrived damaged.",
        "createdAt": "2026-05-20T12:00:00Z"
      },
      {
        "role": "assistant",
        "content": "Please upload a clear photo of the damaged shoes.",
        "createdAt": "2026-05-20T12:00:00Z"
      }
    ]
  }
]
```

## Update Ticket Status

```http
PATCH /api/tickets/{ticket_id}
```

Request:

```json
{
  "status": "Approved",
  "suggestedAction": "Approve refund",
  "evidenceProvided": true
}
```

## Dashboard Overview

```http
GET /api/dashboard/overview
```

Response:

```json
{
  "metrics": {
    "totalChats": 1286,
    "aiResolved": 1092,
    "refundsPrevented": 247500,
    "exchangesSuggested": 133,
    "humanEscalations": 1,
    "averageResponseTime": "3.2s",
    "totalReturns": 349,
    "highRiskFlagged": 1,
    "refundValueSaved": 187500
  }
}
```

## Create Ticket

```http
POST /api/tickets
```

Request:

```json
{
  "orderId": "ORD-1045",
  "customerId": "CUS-501",
  "issue": "Damaged item",
  "riskLevel": "High",
  "riskScore": 75,
  "suggestedAction": "Request photo proof and escalate if unclear"
}
```

Response:

```json
{
  "id": "T-104",
  "status": "Evidence Required"
}
```

## Error Shape

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "No order was found for the provided order ID."
  }
}
```
