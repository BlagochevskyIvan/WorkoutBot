from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ProgramResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name: str
    description : Optional[str] = None

class ProgramDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name: str
    description : Optional[str] = None

class ProgramCreate(BaseModel):
    name: str = Field(min_lenght=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)

