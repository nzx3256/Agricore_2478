from pydantic import BaseModel, ConfigDict, Field

class FarmerBase(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    farm_id: int

class FarmerCreate(FarmerBase):
    pass

class FarmerRead(FarmerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
