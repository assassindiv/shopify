# ReturnShield Frontend

Customer chat and merchant dashboard UI for the ReturnShield MVP.

## Current Static Screens

- `customer.html`: customer-facing support chat connected to the backend return-check API.
- `merchant.html`: merchant console and dashboard mockup.

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

## Planned Areas

- `src/components`: reusable UI components
- `src/pages`: dashboard and chat screens
- `src/lib`: API client and shared utilities
