from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.report_repo import ReportRepository
from app.schemas.report import ByCategoryResponse, MonthlyResponse, SummaryResponse

router = APIRouter(prefix="/reports", tags=["reports"])


def get_report_repo(session: Annotated[AsyncSession, Depends(get_db)]) -> ReportRepository:
    return ReportRepository(session)


ReportRepoDep = Annotated[ReportRepository, Depends(get_report_repo)]


@router.get("/summary", response_model=SummaryResponse)
async def get_summary(repo: ReportRepoDep) -> SummaryResponse:
    return await repo.get_summary()


@router.get("/monthly", response_model=MonthlyResponse)
async def get_monthly(repo: ReportRepoDep) -> MonthlyResponse:
    return await repo.get_monthly()


@router.get("/by-category", response_model=ByCategoryResponse)
async def get_by_category(repo: ReportRepoDep) -> ByCategoryResponse:
    return await repo.get_by_category()
