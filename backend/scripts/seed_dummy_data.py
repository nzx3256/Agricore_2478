
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models import Equipment, Farmer, Farm, FieldJob, ServiceReport
from app.models import EquipmentStatus, FieldJobPriority, FieldJobStatus


async def seed_dummy_data(session: AsyncSession) -> None:
    session.add_all([
        Farm(id=1, name="Jolly Ol' Ranch", location_region="Kansas", capacity=10),
        Farm(id=2, name="Farmhouse", location_region="Nevada", capacity=50)
    ])
    session.add_all([
        Equipment(serial_number="HACH1", model="Hachet", status=EquipmentStatus.IDLE, fuel_level=100, farm_id=1),
        Equipment(serial_number="HOE1", model="Hoe", status=EquipmentStatus.MAINTENANCE, fuel_level=56.0, farm_id=1),
        Equipment(serial_number="BRM", model="Broom", status=EquipmentStatus.IN_MISSION, fuel_level=76.6, farm_id=2),
        Equipment(serial_number="SHOV1", model="Shovel", status=EquipmentStatus.IN_MISSION, fuel_level=40.2, farm_id=2),
        Equipment(serial_number="R1", model="Rake", status=EquipmentStatus.IN_MISSION, fuel_level=25.2, farm_id=2)
    ])
    session.add_all([
        Farmer(full_name="Billy Bob Jankins", farm_id=1),
        Farmer(full_name="Tom Sawyer", farm_id=1),
        Farmer(full_name="Lennie", farm_id=2),
        Farmer(full_name="George", farm_id=2),
        Farmer(full_name="Curley's Wife", farm_id=2),
        Farmer(full_name="Slim", farm_id=2)
    ])
    session.add_all([
        FieldJob(title="Barn sweeping",priority=FieldJobPriority.LOW,status=FieldJobStatus.PENDING,equipment_id=3,farmer_id=3),
        FieldJob(title="Grave Digging",priority=FieldJobPriority.CRITICAL,status=FieldJobStatus.IN_PROGRESS,equipment_id=4,farmer_id=4),
        FieldJob(title="Field Raking",priority=FieldJobPriority.MEDIUM,status=FieldJobStatus.COMPLETED,equipment_id=5,farmer_id=1)
    ])
    session.add_all([
        ServiceReport(file_url="dumy", notes="Lennie still hasn't swept the barn", field_job_id=1),
        ServiceReport(file_url="dumy", notes="Hey! Who raked the fields? (Ooooo... spooky)", field_job_id=3)
    ])
    await session.commit()

async def main() -> None:
    async with AsyncSessionLocal() as session:
        await seed_dummy_data(session)

if __name__ == "__main__":
    asyncio.run(main())
