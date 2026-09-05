from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.core.database import Base

class Trade(Base):
    __tablename__ = "paper_trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, default="UNKNOWN")
    entry_time = Column(DateTime, index=True)
    exit_time = Column(DateTime, nullable=True)
    signal = Column(String) # CALL or PUT
    entry_price = Column(Float)
    exit_price = Column(Float, nullable=True)
    stake = Column(Float)
    payout = Column(Float)
    result = Column(String, nullable=True) # WIN, LOSS, TIE, PENDING
    profit = Column(Float, nullable=True)
    strategy_version = Column(String)
