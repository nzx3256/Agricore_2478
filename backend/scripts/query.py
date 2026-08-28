from asyncio import run as async_run

from sqlalchemy import Case, Float, and_, func, select, cast
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import Equipment, FieldJob, Farmer, Farm
from app.models import EquipmentStatus, FieldJobStatus

async def find_low_fuel_level(session: AsyncSession, threshold: float) -> list[Equipment]:
    stmt = (
        select(Equipment)
        .where(and_(Equipment.status != EquipmentStatus.OFFLINE, Equipment.fuel_level <= threshold))
        .order_by(Equipment.model, Equipment.id)
    )
    results = await session.execute(stmt)
    return list(results.scalars().all())

async def find_colocation_discrepencies(session: AsyncSession) -> list[tuple[int, str,int,int]]:
    stmt = (
        select(FieldJob.id, FieldJob.title, Farmer.farm_id, Equipment.farm_id)
        .join(Equipment)
        .join(Farmer)
        .where(Farmer.farm_id != Equipment.farm_id)
        .order_by(FieldJob.title)
    )
    results = await session.execute(stmt)
    return list(results.tuples())

async def get_reliability_metrics(session: AsyncSession) -> list[tuple[int,int, str]]:
    completed_count = \
        func.sum(Case((FieldJob.status == FieldJobStatus.COMPLETED,1), else_=0))
    failed_count = \
        func.sum(Case((FieldJob.status == FieldJobStatus.FAILED,1),else_=0))
    stmt = (
        select(completed_count.label("completed_count"), 
           failed_count.label("failed_count"), Equipment.model)
        .join(FieldJob)
        .group_by(Equipment.model)
    )
    results = await session.execute(stmt)
    return list(results.tuples())

async def get_maintenance_flags(session: AsyncSession) -> list[tuple[str, float]]:
    maintenance_percent = cast(func.sum(Case((Equipment.status == EquipmentStatus.MAINTENANCE, 1), else_=0)), Float)/func.count(Equipment.id)
    stmt = (
        select(Farm.name.label("farm name"),maintenance_percent.label("equipment in maintenance (%)"))
        .join(Equipment)
        .group_by(Farm.name)
        .having(maintenance_percent > 0.3)
    )
    results = await session.execute(stmt)
    return list(results.tuples())

async def main():
    async with AsyncSessionLocal() as session:
        THRESHOLD = 50
        print("\033[32m== Low Battery Alerts ==\033[0m")
        alerts = await find_low_fuel_level(session, THRESHOLD)
        if not alerts:
            print(f"\tThere is no equipment with fuel level <= {THRESHOLD}")
        for equipment in alerts:
            print("\t",equipment)
        print("\033[32m== Colocation Discrepencies ==\033[0m")
        discrepencies = await find_colocation_discrepencies(session)
        if not discrepencies:
            print("\tThere are no discrepencies")
        for disc in discrepencies:
            job_id, title, fer_farm_id, equip_farm_id = disc
            print(f"\tdiscrepency: job_id={job_id}, title={title!r}, "
                  f"Farmer.farm_id={fer_farm_id}, Equipment.farm_id={equip_farm_id}")
        print("\033[32m== Reliability Metrics ==\033[0m")
        metrics = await get_reliability_metrics(session)
        if not metrics:
            print("\tNo metrics to display")
        for metric in metrics:
            completed, failed, model = metric
            print(f"\tmetric: completed={completed}, failed={failed}, models={model}")
        print("\033[32m== Maintenance Flags ==\033[0m")
        flags = await get_maintenance_flags(session)
        if not flags:
            print("\tNo farms with 30% equipment maintenance")
        for flag in flags:
            farm_name, percent = flag
            print(f"\tflag: farm_name={farm_name!r}, maintenance_percent={percent}")

if __name__ == "__main__":
    async_run(main())
