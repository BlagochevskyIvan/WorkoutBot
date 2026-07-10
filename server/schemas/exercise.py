from pydantic import BaseModel

class ExerciseResponse(BaseModel):
    id: int
    name: str

class ExerciseCreate(BaseModel):
    name: str