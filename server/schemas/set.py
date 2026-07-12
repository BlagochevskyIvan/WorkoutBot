from pydantic import BaseModel, ConfigDict

class SetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    weight : float
    reps : int

class SetCreate(BaseModel):
    weight : float
    reps : int
