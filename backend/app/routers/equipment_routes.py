import traceback
import sys

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import from_

from app.dependencies import get_current_user, get_db, require_role
from app.models import Equipment, FieldJob, FieldJobStatus, User, UserRole
from app.schemas.equipment_schemas import EquipmentCreate, EquipmentRead, EquipmentReliabilityMetrics

router = APIRouter(prefix="/equipment", tags=["equipment"])

@router.get("", response_model=list[EquipmentRead])
async def list_equipment(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> list[Equipment]:
    results = await db.execute(select(Equipment))
    return list(results.scalars().all())

@router.get("/reliability_metrics", response_model=list[EquipmentReliabilityMetrics])
async def get_reliability_metrics(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> list[EquipmentReliabilityMetrics]:
    completed_part = func.sum(case(
        (FieldJob.status == FieldJobStatus.COMPLETED, 1),
        else_=0
    ))
    failed_part = func.sum(case(
        (FieldJob.status == FieldJobStatus.FAILED, 1),
        else_=0
    ))
    concatfield = func.concat(completed_part, ":", failed_part)
    stmt = (
        select(
            Equipment.id.label("equipment_id"),
            Equipment.model.label("equipment_model"),
            concatfield.label("completed_failed_ratio")
        )
        .join(FieldJob, FieldJob.equipment_id == Equipment.id)
        .group_by(Equipment.model, Equipment.id)
    )
    results = await db.execute(stmt)
    return [EquipmentReliabilityMetrics.model_validate(result) 
                for result in results.mappings().all()]

@router.get("/{equipment_id}", response_model=EquipmentRead)
async def get_equipment(
    equipment_id: int, 
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> Equipment: 
    results = await db.get(Equipment, equipment_id)
    if results is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No equipment with id equipment_id")
    return results

@router.post("", response_model=EquipmentRead, status_code=status.HTTP_201_CREATED)
async def create_equipment(
    payload: EquipmentCreate, 
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.FARM_OPERATORS_ADMIN))
) -> Equipment:
    equipment = Equipment(**payload.model_dump())
    db.add(equipment)
    await db.commit()
    await db.refresh(equipment)
    return equipment
