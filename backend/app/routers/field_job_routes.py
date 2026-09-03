from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db, require_role
from app.schemas.field_job_schemas import DiscrepencyRead, FieldJobCreate, FieldJobRead, JobStatusUpdate
from app.models import FieldJob, FieldJobStatus, Farmer, Equipment, User, UserRole

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get(path="", response_model=list[FieldJobRead])
async def list_all_jobs(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> list[FieldJob]:
    results = await db.execute(select(FieldJob))
    return list(results.scalars().all())

@router.get(path="/discrepencies", response_model=list[DiscrepencyRead])
async def get_colocation_discrepencies(
    db: AsyncSession = Depends(get_db), 
    _: User = Depends(get_current_user)
):
    stmt = (
        select(
            FieldJob.id.label("job_id"), FieldJob.title.label("job_title"),
            Equipment.farm_id.label("farmer_farm_id"), Farmer.farm_id.label("equipment_farm_id")
        ).join(Equipment).join(Farmer)
        .where(Equipment.farm_id != Farmer.farm_id)
    )
    results = await db.execute(stmt)
    return [DiscrepencyRead.model_validate(result)
            for result in results.mappings().all()]

@router.get(path="/{job_id}", response_model=FieldJobRead)
async def get_job(
    job_id:int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> FieldJob:
    job = await db.get(FieldJob, job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No job with id {job_id}"
        )
    return job

@router.patch(path="/{job_id}/status", response_model=FieldJobRead)
async def update_field_job_status(
    job_id: int,
    payload: JobStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.FARM_OPERATORS_ADMIN, UserRole.FIELD_HAND))
) -> FieldJob:
    job = await db.get(FieldJob, job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No job with id {job_id}"
        )
    if payload.status == FieldJobStatus.COMPLETED:
        job.mark_completed()
    elif payload.status == FieldJobStatus.FAILED:
        job.mark_failed()
    else:
        job.status = payload.status
    await db.commit()
    await db.refresh(job)
    return job

@router.post(path="", response_model=FieldJobRead, status_code=status.HTTP_201_CREATED)
async def create_field_job(
    payload: FieldJobCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.FARM_OPERATORS_ADMIN))
) -> FieldJob:
    job = FieldJob(**payload.model_dump())
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job
