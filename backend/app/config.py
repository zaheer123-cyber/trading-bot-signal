from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Trading Signal & Backtesting Platform"
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./trading.db"
    
    # Risk Management & Paper Trading
    INITIAL_BALANCE: float = 1000.0
    TRADE_AMOUNT: float = 10.0
    PAYOUT: float = 0.80
    MAX_DAILY_LOSS: float = 50.0
    
    # Strategy Parameters
    SIGNAL_THRESHOLD: int = 70
    EMA_FAST: int = 20
    EMA_SLOW: int = 50
    RSI_PERIOD: int = 14
    ATR_PERIOD: int = 14
    EXPIRY_CANDLES: int = 1
    
    # Minimum EMA separation threshold (percentage)
    EMA_DISTANCE_PERCENT_MIN: float = 0.05
    # Minimum ATR limit for trading
    ATR_MIN_VOLATILITY: float = 0.0001
    
    # RSI Thresholds
    RSI_OVERBOUGHT: int = 70
    RSI_OVERSOLD: int = 30
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
