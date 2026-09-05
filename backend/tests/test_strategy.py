import pytest
import pandas as pd
from app.services.indicators import Indicators
from app.services.strategy import Strategy
from app.services.signal_engine import SignalEngine

def test_ema_calculation():
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    df = Indicators.add_ema(df, period=3)
    assert 'ema_3' in df.columns
    assert not df['ema_3'].isnull().all()

def test_signal_engine_no_trade_on_low_volatility():
    # Volatility too low
    row = pd.Series({
        'ema_20': 105,
        'ema_50': 100,
        'rsi_14': 60,
        'atr_14': 0.000001, # Below threshold
        'close': 106,
        'ema_distance_pct': 5
    })
    
    signal = SignalEngine.generate_signal(row)
    assert signal['signal'] == "NO_TRADE"
    assert "Volatility too low (ATR)" in signal['reasons']

def test_signal_engine_call():
    row = pd.Series({
        'ema_20': 110,
        'ema_50': 100,
        'rsi_14': 60,
        'atr_14': 1.5,
        'close': 111,
        'ema_distance_pct': 9.0,
        'support': 110,
        'bullish_engulfing': True
    })
    
    signal = SignalEngine.generate_signal(row)
    assert signal['signal'] == "CALL"
    assert signal['score'] >= 70
