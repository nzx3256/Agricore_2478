from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.equipment import Equipment
from app.schemas.equipment_schemas import EquipmentCreate, EquipmentRead

router = APIRouter(prefix="/equipment", tags=["equipment"])

@router.get("", response_model=list[EquipmentRead])
async def list_equipment(db: AsyncSession = Depends(get_db)) -> list[Equipment]:
    results = await db.execute(select(Equipment))
    return list(results.scalars().all())

@router.get("/{equipment_id}", response_model=EquipmentRead)
async def get_equipment(equipment_id: int, db: AsyncSession = Depends(get_db)) -> Equipment: 
    results = await db.get(Equipment, equipment_id)
    if results is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No equipment with id equipment_id")
    return results

@router.post("", response_model=EquipmentRead, status_code=status.HTTP_201_CREATED)
async def create_equipment(payload: EquipmentCreate, db: AsyncSession = Depends(get_db)) -> Equipment:
    equipment = Equipment(**payload.model_dump())
    db.add(equipment)
    await db.commit()
    await db.refresh(equipment)
    return equipment
