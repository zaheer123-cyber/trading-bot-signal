from pydantic import BaseModel
from typing import List, Optional

class SignalRequest(BaseModel):
    filepath: str

class SignalResponse(BaseModel):
    signal: str
    score: int
    confidence_label: str
    reasons: List[str]
