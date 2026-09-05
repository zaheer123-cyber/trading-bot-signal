from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.core.database import Base

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, default="UNKNOWN")
    timestamp = Column(DateTime, index=True)
    signal_type = Column(String, index=True) # CALL, PUT, NO_TRADE
    score = Column(Integer)
    confidence_label = Column(String)
    reasons = Column(JSON) # Store list of reasons
    strategy_version = Column(String)
    
    # Store indicator values for analysis
    close_price = Column(Float)
    ema_fast = Column(Float, nullable=True)
    ema_slow = Column(Float, nullable=True)
    rsi = Column(Float, nullable=True)
    atr = Column(Float, nullable=True)
    support = Column(Float, nullable=True)
    resistance = Column(Float, nullable=True)
