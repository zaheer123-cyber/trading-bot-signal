from pydantic import BaseModel
from typing import Dict, Any

class BacktestRequest(BaseModel):
    filepath: str
    # Settings overrides could be added here
    
class BacktestResponse(BaseModel):
    metrics: Dict[str, Any]
    # In a real app we might not want to return all trades in one payload, but for this scale it's fine.
    trades_count: int
