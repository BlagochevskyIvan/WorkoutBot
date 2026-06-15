from pydantic import BaseModel

class ExerciseResponse(BaseModel):
    id: int
    name: str