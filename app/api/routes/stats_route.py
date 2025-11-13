from app.api.routes.utils.error_response import exception_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db
from app.services.stats_service import StatsService

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/total_sessions/{user_id}", response_model=dict[str, int])
async def total_sessions(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await exception_service(StatsService.get_total_sessions, user_id, db)


@router.get("/average_score/{user_id}", response_model=dict[str, float])
async def average_score(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await exception_service(StatsService.get_average_score, user_id, db)



@router.get("/total_shots/{user_id}", response_model=dict[str, int])
async def total_shots(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await exception_service(StatsService.get_total_shots, user_id, db)


@router.get("/best_session/{user_id}", response_model=dict[str, str | float])
async def best_session(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await exception_service(StatsService.get_best_session, user_id, db)



@router.get("/last_session_date/{user_id}", response_model=dict[str, str])
async def last_session_date(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await exception_service(StatsService.get_last_session_date, user_id, db)
