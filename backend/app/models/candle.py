from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.database import Base

class Candle(Base):
    __tablename__ = "candles"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, default="UNKNOWN")
    timeframe = Column(String, index=True, default="1m")
    timestamp = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float, nullable=True)
