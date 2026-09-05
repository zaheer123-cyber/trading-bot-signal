from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_market, routes_signals, routes_backtest, routes_trades, routes_stats
from app.core.database import engine, Base
from app.config import settings
from app.core.logging_config import setup_logging
import logging

# Initialize DB (in a real app, use alembic)
Base.metadata.create_all(bind=engine)

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Trading Signal & Backtesting Platform (Educational Research Only)"
)

# CORS config — allow Vite dev server in development; restrict in production
ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
if settings.APP_ENV == "development":
    # Only allow known dev origins, not wildcard
    pass

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

app.include_router(routes_market.router, prefix="/api/market", tags=["Market"])
app.include_router(routes_signals.router, prefix="/api/signals", tags=["Signals"])
app.include_router(routes_backtest.router, prefix="/api/backtest", tags=["Backtest"])
app.include_router(routes_trades.router, prefix="/api/trades", tags=["Trades"])
app.include_router(routes_stats.router, prefix="/api/stats", tags=["Stats"])

@app.on_event("startup")
def on_startup():
    logger.info(f"Started {settings.APP_NAME} in {settings.APP_ENV} mode.")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
