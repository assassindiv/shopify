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
