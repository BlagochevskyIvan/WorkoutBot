from pydantic import BaseModel, ConfigDict

class WorkoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int | None = None
    name : str | None = None