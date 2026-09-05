from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_trades():
    # Placeholder for returning paper trades from DB
    return []
