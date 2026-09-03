from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import FieldJobPriority, FieldJobStatus;

class FieldJobBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    priority: FieldJobPriority
    status: FieldJobStatus = FieldJobStatus.PENDING
    equipment_id: int
    farmer_id: int

class FieldJobCreate(FieldJobBase):
    pass

class JobStatusUpdate(BaseModel):
    status: FieldJobStatus

class FieldJobRead(FieldJobBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class DiscrepencyRead(BaseModel):
    job_id: int
    job_title: str = Field(min_length=1, max_length=100)
    farmer_farm_id: int
    equipment_farm_id: int
    model_config = ConfigDict(from_attributes=True)
