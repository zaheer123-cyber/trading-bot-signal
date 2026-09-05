from fastapi import APIRouter, HTTPException
from app.schemas.signal import SignalRequest, SignalResponse
from app.services.data_loader import DataLoader
from app.services.strategy import Strategy
from app.services.signal_engine import SignalEngine
import os

router = APIRouter()

@router.post("/signals/analyze", response_model=SignalResponse)
def analyze_signal(request: SignalRequest):
    if not os.path.exists(request.filepath):
        raise HTTPException(status_code=404, detail="Data file not found")
        
    try:
        # Load and prepare data
        df = DataLoader.load_csv(request.filepath)
        df_enriched = Strategy.prepare_data(df)
        
        # Analyze the latest candle
        latest_row = df_enriched.iloc[-1]
        signal = SignalEngine.generate_signal(latest_row)
        
        return signal
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@router.get("/signals/recent")
def get_recent_signals():
    # Placeholder for fetching recent signals from DB
    return []
