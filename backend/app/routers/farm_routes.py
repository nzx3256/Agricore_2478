from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import case, Float, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db, require_role
from app.schemas.farm_schemas import FarmMaintenancePercentage, FarmRead, FarmCreate
from app.models import Farm, User, Equipment, EquipmentStatus, UserRole

router = APIRouter(prefix="/farms", tags=["farms"])

@router.get("", response_model=list[FarmRead])
async def list_farms(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> list[Farm]:
    results = await db.execute(select(Farm))
    return list(results.scalars().all())

@router.get("/maintenance_flags", response_model=list[FarmMaintenancePercentage])
async def get_maintenance_flags(
    threshold: float,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> list[FarmMaintenancePercentage]:
    maintenance_count = (
        func.sum(case((Equipment.status == EquipmentStatus.MAINTENANCE, 1), else_=0)) .cast(Float)
    )
    percentage_field = maintenance_count/func.count(Equipment.id)
    stmt = (
        select(
            Farm.id.label("farm_id"),
            Farm.name.label("farm_name"),
            percentage_field.label("percent_maintenance"),
        )
        .join(Equipment)
        .group_by(Farm.name, Farm.id)
        .having(percentage_field >= threshold)
    )
    results = await db.execute(stmt)
    return [FarmMaintenancePercentage.model_validate(result)
            for result in results.mappings().all()]

@router.get("/{farm_id}", response_model=FarmRead)
async def get_farm(
    farm_id: int, 
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
) -> Farm:
    farm = await db.get(Farm, farm_id)
    if farm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Farm with id {farm_id}")
    return farm

@router.post("", response_model=FarmRead, status_code=status.HTTP_201_CREATED)
async def create_farm(
    payload: FarmCreate, 
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.FARM_OPERATORS_ADMIN))
) -> Farm:
    farm = Farm(**payload.model_dump())
    db.add(farm)
    await db.commit()
    await db.refresh(farm)
    return farm
