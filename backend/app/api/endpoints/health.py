from fastapi import APIRouter
from app.schemas.base import HealthCheck

router = APIRouter()


@router.get("/health", response_model=HealthCheck, tags=["health"])
async def read_health():
    return {"status": "ok"}
