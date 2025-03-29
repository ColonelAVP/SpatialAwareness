from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from app.db import Base

class Polygon(Base):
    __tablename__ = "polygons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    geom = Column(Geometry(geometry_type="POLYGON", srid=4326))