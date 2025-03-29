from pydantic import BaseModel
from typing import Any

class PolygonBase(BaseModel):
    name: str
    geom: dict

class PolygonCreate(PolygonBase):
    pass

class PolygonRead(PolygonBase):
    id: int

    class Config:
        orm_mode = True