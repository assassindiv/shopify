# ReturnShield Frontend

Customer chat and merchant dashboard UI for the ReturnShield MVP.

## Current Static Screens

- `customer.html`: customer-facing support chat connected to the backend return-check API.
- `merchant.html`: merchant console connected to live dashboard metrics and tickets.

Open `customer.html` in the browser after starting the backend:

```bash
cd backend
uvicorn app.main:app --reload
```

If the browser shows `Failed to fetch`, restart the backend after pulling the latest CORS change. You can also serve the static frontend from the project root:

```bash
python -m http.server 5500
```

Then open:

```text
http://localhost:5500/frontend/customer.html
```

Merchant console:

```text
http://localhost:5500/frontend/merchant.html
```

## End-To-End Demo

1. Start the backend with `GROQ_API_KEY` set.
2. Open `customer.html`.
3. Click `Run suspicious refund demo`.
4. Open `merchant.html`.
5. The ticket queue should show `T-104` as a high-risk damaged-item case.

## Planned Areas

- `src/components`: reusable UI components
- `src/pages`: dashboard and chat screens
- `src/lib`: API client and shared utilities
