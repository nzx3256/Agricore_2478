from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class ServiceReportBase(BaseModel):
    file_url: str = Field(min_length=1)
    notes: str = Field(min_length=1)
    field_job_id: int
    created_at: datetime = Field()

class ServiceReportCreate(ServiceReportBase):
    pass

class ServiceReportRead(ServiceReportBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
