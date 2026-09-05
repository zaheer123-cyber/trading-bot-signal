from fastapi import APIRouter, HTTPException
from app.schemas.signal import SignalRequest, SignalResponse
from app.services.data_loader import DataLoader
from app.services.strategy import Strategy
from app.services.signal_engine import SignalEngine
from app.config import settings
import os

router = APIRouter()

def _get_default_filepath() -> str:
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    return os.path.join(base, "data", "raw", "sample.csv")

@router.post("/analyze", response_model=SignalResponse)
def analyze_signal(request: SignalRequest):
    if not os.path.exists(request.filepath):
        raise HTTPException(status_code=404, detail="Data file not found")
    try:
        df = DataLoader.load_csv(request.filepath)
        df_enriched = Strategy.prepare_data(df)
        latest_row = df_enriched.iloc[-1]
        signal = SignalEngine.generate_signal(latest_row)
        return signal
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/latest")
def get_latest_signal():
    """Return the latest signal computed from the sample dataset."""
    filepath = _get_default_filepath()
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="No data available. Add a CSV to data/raw/sample.csv")

    try:
        df = DataLoader.load_csv(filepath)
        df_enriched = Strategy.prepare_data(df)
        latest_row = df_enriched.iloc[-1]
        signal_data = SignalEngine.generate_signal(latest_row)

        ema_fast = float(latest_row.get(f"ema_{settings.EMA_FAST}", 0) or 0)
        ema_slow = float(latest_row.get(f"ema_{settings.EMA_SLOW}", 0) or 0)

        trend = "NEUTRAL"
        if ema_fast > ema_slow:
            trend = "BULLISH"
        elif ema_fast < ema_slow:
            trend = "BEARISH"

        return {
            "signal": signal_data["signal"],
            "score": signal_data["score"],
            "trend": trend,
            "rsi": round(float(latest_row.get(f"rsi_{settings.RSI_PERIOD}", 0) or 0), 2),
            "ema_fast": round(ema_fast, 4),
            "ema_slow": round(ema_slow, 4),
            "atr": round(float(latest_row.get(f"atr_{settings.ATR_PERIOD}", 0) or 0), 5),
            "timestamp": str(latest_row.get("timestamp")),
            "reasons": signal_data["reasons"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent")
def get_recent_signals():
    return []
