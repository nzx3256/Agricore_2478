from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.farmer import Farmer
from app.schemas.farmer_schemas import FarmerCreate, FarmerRead
from app.dependencies import get_db

router = APIRouter(prefix="/farmers", tags=["farmers"])

@router.get("", response_model=list[FarmerRead])
async def list_farmers(db: AsyncSession = Depends(get_db)) -> list[Farmer]:
    results = await db.execute(select(Farmer))
    return list(results.scalars().all())

@router.get("/{farmer_id}", response_model=FarmerRead)
async def get_farmer(farmer_id:int, db: AsyncSession = Depends(get_db)) -> Farmer:
    farmer = await db.get(Farmer, farmer_id)
    if farmer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No farmer with id {farmer_id}")
    return farmer

@router.post("", response_model=FarmerRead, status_code=status.HTTP_201_CREATED)
async def create_farmer(payload: FarmerCreate, db: AsyncSession = Depends(get_db)) -> Farmer:
    farmer = Farmer(**payload.model_dump())
    db.add(farmer)
    await db.commit()
    await db.refresh(farmer)
    return farmer
