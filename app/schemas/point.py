from pydantic import BaseModel
from typing import Any

class PointBase(BaseModel):
    name: str
    geom: dict  # Expecting GeoJSON format

class PointCreate(PointBase):
    pass

class PointRead(PointBase):
    id: int

    class Config:
        orm_mode = True