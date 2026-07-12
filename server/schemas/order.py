from pydantic import BaseModel


class OrderUpdate(BaseModel):
    ids: list[int]
