from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, orders, products, returns, risk, tickets
from app.core.config import API_PREFIX, APP_NAME
from app.core.errors import AppError, app_error_handler


app = FastAPI(title="ReturnShield API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)

app.include_router(health.router, prefix=API_PREFIX)
app.include_router(products.router, prefix=API_PREFIX)
app.include_router(orders.router, prefix=API_PREFIX)
app.include_router(risk.router, prefix=API_PREFIX)
app.include_router(returns.router, prefix=API_PREFIX)
app.include_router(tickets.router, prefix=API_PREFIX)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": APP_NAME, "docs": "/docs"}
