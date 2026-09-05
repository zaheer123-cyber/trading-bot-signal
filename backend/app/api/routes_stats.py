from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_stats():
    # Placeholder for general stats
    return {"message": "Stats route"}
    
@router.get("/equity")
def get_equity():
    # Placeholder for equity curve data
    return []
