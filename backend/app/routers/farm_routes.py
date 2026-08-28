from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.farm_schemas import FarmRead, FarmCreate
from app.models import Farm

router = APIRouter(prefix="/farms", tags=["farms"])

@router.get("", response_model=list[FarmRead])
async def list_farms(db: AsyncSession = Depends(get_db)) -> list[Farm]:
    results = await db.execute(select(Farm))
    return list(results.scalars().all())

@router.get("/{farm_id}", response_model=FarmRead)
async def get_farm(farm_id: int, db: AsyncSession = Depends(get_db)) -> Farm:
    farm = await db.get(Farm, farm_id)
    if farm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Farm with id {farm_id}")
    return farm

@router.post("", response_model=FarmRead, status_code=status.HTTP_201_CREATED)
async def create_farm(payload: FarmCreate, db: AsyncSession = Depends(get_db)) -> Farm:
    farm = Farm(**payload.model_dump())
    db.add(farm)
    await db.commit()
    await db.refresh(farm)
    return farm
