from pydantic import BaseModel, ConfigDict

class ExerciseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class ExerciseCreate(BaseModel):
    name: str
