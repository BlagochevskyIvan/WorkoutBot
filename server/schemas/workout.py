from pydantic import BaseModel, ConfigDict, Field

class WorkoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    name : str

class WorkoutCreate(BaseModel):
    name: str = Field(min_lenght=1, max_length=50)
    