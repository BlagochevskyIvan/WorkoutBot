from pydantic import BaseModel, ConfigDict
from datetime import date


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id : int
    username : str 
    gender : str | None = None
    experience : str | None = None
    place : str | None = None
    birth_date : date | None = None