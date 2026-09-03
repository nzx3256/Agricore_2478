from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.report_schemas import ServiceReportRead, ServiceReportCreate
from app.models import ServiceReport, User, UserRole
from app.dependencies import get_current_user, get_db, require_role

router = APIRouter(prefix="/reports", tags=["reports"]);

@router.get("", response_model=list[ServiceReportRead])
async def list_service_reports(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> list[ServiceReport]:
    results = await db.execute(select(ServiceReport))
    return list(results.scalars().all())

@router.get("/{report_id}", response_model=ServiceReportRead)
async def get_service_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> ServiceReport: 
    result = await db.get(ServiceReport, report_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No report with id {report_id} found"
        )
    return result

@router.post("", response_model=ServiceReportRead)
async def create_service_report(
    payload: ServiceReportCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.FARM_OPERATORS_ADMIN, 
        UserRole.FIELD_HAND))
) -> ServiceReport:
    report = ServiceReport(**payload.model_dump())
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report
