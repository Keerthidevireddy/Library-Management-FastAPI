from fastapi import APIRouter, Depends
from app.middlewares.auth_guard import get_current_user
from app.services.dashboard_service import get_dashboard_counts

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/counts")
def counts(user=Depends(get_current_user)):
    return get_dashboard_counts(user)
