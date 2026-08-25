from asyncio import run as async_run
from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import Equipment, FieldJob, Farmer, EquipmentStatus

async def find_low_fuel_level(session: AsyncSession, threshold: float) -> list[Equipment]:
    stmt = (
            select(Equipment)
            .where(and_(Equipment.status != EquipmentStatus.OFFLINE, Equipment.fuel_level <= threshold))
            .order_by(Equipment.model, Equipment.id)
    )
    results = await session.execute(stmt)
    return list(results.scalars().all())

async def find_colocation_discrepencies(session: AsyncSession) -> list[Any]:
    stmt = (
            select(FieldJob.id, FieldJob.title, Farmer.farm_id, Equipment.farm_id)
            .join(Equipment)
            .join(Farmer)
            .where(Farmer.farm_id != Equipment.farm_id)
            .order_by(FieldJob.title)
    )
    results = await session.execute(stmt)
    return list(results.scalars().all())

async def main():
    async with AsyncSessionLocal() as session:
        THRESHOLD = 20
        print("\033[32m== Low Battery Alerts ==\033[0m")
        alerts = await find_low_fuel_level(session, THRESHOLD)
        if not alerts:
            print(f"There is no equipment with fuel level <= {THRESHOLD}")
        for equipment in alerts:
            print("",equipment)
        print("\033[32m== Colocation Discrepencies ==\033[0m")
        discrepencies = await find_colocation_discrepencies(session)
        if not discrepencies:
            print(f"There are no discrepencies")
        for disc in discrepencies:
            print(f" discrepency: job_id={disc[0]}, title={disc[1]}, "
                  f"Farmer.farm_id={disc[2]}, Equipment.farm_id[3]")

if __name__ == "__main__":
    async_run(main())
