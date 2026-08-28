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

class FieldJobRead(FieldJobBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
