from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Text, String

from app.models import EquipmentStatus

class EquipmentBase(BaseModel):
    serial_number: str
    model: str = Field(min_length=1, max_length=100)
    status: EquipmentStatus = EquipmentStatus.IDLE
    fuel_level: float = Field(ge=0.0, le=100.0)
    farm_id: int

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentRead(EquipmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class EquipmentReliabilityMetrics(BaseModel):
    equipment_id: int
    equipment_model: str = Field(min_length=1, max_length=100)
    completed_failed_ratio: str = Field(min_length=3)
    model_config = ConfigDict(from_attributes=True)
