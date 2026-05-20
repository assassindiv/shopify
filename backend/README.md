# ReturnShield Backend

FastAPI service for mock Shopify data, return eligibility checks, risk scoring, and support ticket creation.

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs:

```text
http://localhost:8000/docs
```

## AI Setup

The chat endpoint uses Groq's OpenAI-compatible chat API.

Create `backend/.env`:

```text
GROQ_API_KEY=your_groq_api_key
```

Optional model override:

```text
GROQ_MODEL=llama-3.1-8b-instant
```

Then start the API:

```bash
uvicorn app.main:app --reload
```

## Planned Modules

- `app/api`: HTTP route handlers
- `app/core`: app configuration and shared settings
- `app/models`: request/response schemas
- `app/services`: business logic for orders, returns, risk, and tickets
- `app/data`: mock products, orders, customers, policies, and tickets

## Demo Request

```http
POST /api/returns/check
```

```json
{
  "orderId": "ORD-1045",
  "customerEmail": "aarav@example.com",
  "reason": "damaged_item",
  "photoProofProvided": false
}
```

## AI Chat Request

```http
POST /api/chat
```

```json
{
  "message": "I want a refund. The shoes arrived damaged. ORD-1045, aarav@example.com",
  "history": []
}
```
