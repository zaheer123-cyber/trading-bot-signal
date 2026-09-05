from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.data_loader import DataLoader
import os

router = APIRouter()

class CandleItem(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None

class MarketResponse(BaseModel):
    candles: List[CandleItem]

@router.get("/candles", response_model=MarketResponse)
def get_candles():
    """Return the last 100 candles from the sample dataset."""
    # Resolve path relative to project root (two levels up from this file)
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    filepath = os.path.join(base, "data", "raw", "sample.csv")

    if not os.path.exists(filepath):
        return {"candles": []}

    try:
        df = DataLoader.load_csv(filepath)
        records = df.tail(100).to_dict("records")
        for r in records:
            r["timestamp"] = str(r["timestamp"])
            if "volume" not in r:
                r["volume"] = None
        return {"candles": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest")
def get_latest_market():
    return {"message": "Use /api/market/candles for OHLC data"}
