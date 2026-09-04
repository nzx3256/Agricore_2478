from pydantic import BaseModel, ConfigDict, Field
from app.schemas.farmer_schemas import FarmerRead

class FarmBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    location_region: str = Field(min_length=1, max_length=150)
    capacity: int
    supervisor_id: int

class FarmCreate(FarmBase):
    pass

class FarmRead(FarmBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class FarmMaintenancePercentage(BaseModel):
    farm_id: int
    farm_name: str = Field(min_length=1, max_length=100)
    percent_maintenance: float
    model_config = ConfigDict(from_attributes=True)

class ReportingLinesRead(BaseModel):
    farmer_id: int
    farmers_name: str
    active_jobs: int
    supervisor_id: int
    model_config = ConfigDict(from_attributes=True)
