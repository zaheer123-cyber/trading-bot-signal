from fastapi import APIRouter, HTTPException
from app.schemas.backtest import BacktestRequest, BacktestResponse
from app.services.data_loader import DataLoader
from app.services.backtester import Backtester
from app.services.metrics import MetricsCalculator
from app.config import settings
import os
import pandas as pd

router = APIRouter()

@router.post("/run", response_model=BacktestResponse)
def run_backtest(request: BacktestRequest):
    if not os.path.exists(request.filepath):
        raise HTTPException(status_code=404, detail="Data file not found")
        
    try:
        df = DataLoader.load_csv(request.filepath)
        
        # Ensure sufficient data
        if len(df) < max(settings.EMA_SLOW, settings.RSI_PERIOD) * 2:
             raise HTTPException(status_code=400, detail="Insufficient data. At least 100 candles are recommended.")
             
        backtester = Backtester(df)
        trades_df = backtester.run()
        
        metrics = MetricsCalculator.calculate_metrics(trades_df, settings.INITIAL_BALANCE)
        
        return {
            "metrics": metrics,
            "trades_count": len(trades_df)
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backtest error: {str(e)}")

@router.get("/{id}")
def get_backtest(id: int):
    # Placeholder for fetching backtest result from DB
    return {"message": "Not implemented"}
