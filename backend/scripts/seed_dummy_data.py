import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import Equipment, Farmer, Farm, FieldJob, ServiceReport, User
from app.models import EquipmentStatus, FieldJobPriority, FieldJobStatus, UserRole
from app.security import hash_password

async def seed_dummy_data(db: AsyncSession) -> None:
    db.add_all([
        Farm(name="Jolly Ol' Ranch", location_region="Kansas", capacity=10, supervisor_id=1),
        Farm(name="Farmhouse", location_region="Nevada", capacity=50, supervisor_id=2)
    ])
    db.add_all([
        Equipment(serial_number="HACH1", model="Hachet", status=EquipmentStatus.IDLE, fuel_level=100, farm_id=1),
        Equipment(serial_number="HOE1", model="Hoe", status=EquipmentStatus.MAINTENANCE, fuel_level=56.0, farm_id=1),
        Equipment(serial_number="BRM", model="Broom", status=EquipmentStatus.IN_MISSION, fuel_level=76.6, farm_id=2),
        Equipment(serial_number="SHOV1", model="Shovel", status=EquipmentStatus.IN_MISSION, fuel_level=40.2, farm_id=2),
        Equipment(serial_number="R1", model="Rake", status=EquipmentStatus.IN_MISSION, fuel_level=25.2, farm_id=2)
    ])
    db.add_all([
        Farmer(full_name="Billy Bob Jankins", farm_id=1),
        Farmer(full_name="Tom Sawyer", farm_id=1),
        Farmer(full_name="Lennie", farm_id=2),
        Farmer(full_name="George", farm_id=2),
        Farmer(full_name="Curley's Wife", farm_id=2),
        Farmer(full_name="Slim", farm_id=2)
    ])
    db.add_all([
        FieldJob(title="Barn sweeping",priority=FieldJobPriority.LOW,status=FieldJobStatus.PENDING,equipment_id=3,farmer_id=3),
        FieldJob(title="Grave Digging",priority=FieldJobPriority.CRITICAL,status=FieldJobStatus.IN_PROGRESS,equipment_id=4,farmer_id=4),
        FieldJob(title="Field Raking",priority=FieldJobPriority.MEDIUM,status=FieldJobStatus.COMPLETED,equipment_id=5,farmer_id=1)
    ])
    db.add_all([
        ServiceReport(file_url="dumy", notes="Lennie still hasn't swept the barn", field_job_id=1),
        ServiceReport(file_url="dumy", notes="Hey! Who raked the fields? (Ooooo... spooky)", field_job_id=3)
    ])
    await db.commit()

async def seed_users(db: AsyncSession):
    db.add_all([
        User(username="admin", hashed_password=hash_password("password"), role=UserRole.FARM_OPERATORS_ADMIN),
        User(username="farmer", hashed_password=hash_password("password"), role=UserRole.FIELD_HAND),
        User(username="auditor", hashed_password=hash_password("password"), role=UserRole.AUDITOR)
    ])
    await db.commit()

async def main() -> None:
    async with AsyncSessionLocal() as session:
        await seed_dummy_data(session)
        await seed_users(session)

if __name__ == "__main__":
    asyncio.run(main())
