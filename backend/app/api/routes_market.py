from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str

@router.get("/health", response_model=HealthResponse)
def get_health():
    return {"status": "ok"}
    
@router.get("/market/latest")
def get_latest_market():
    # Placeholder for returning the latest market conditions
    return {"message": "Market route"}
