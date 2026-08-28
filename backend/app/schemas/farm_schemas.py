from pydantic import BaseModel, ConfigDict, Field

class FarmBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    location_region: str = Field(min_length=1, max_length=150)
    capacity: int

class FarmCreate(FarmBase):
    pass

class FarmRead(FarmBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
