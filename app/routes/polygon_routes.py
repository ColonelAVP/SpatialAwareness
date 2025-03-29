from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.polygon import PolygonCreate, PolygonRead
from app.models.polygon import Polygon
from app.db import SessionLocal
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape, mapping

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PolygonRead)
def create_polygon(polygon: PolygonCreate, db: Session = Depends(get_db)):
    geom = from_shape(shape(polygon.geom), srid=4326)
    db_poly = Polygon(name=polygon.name, geom=geom)
    db.add(db_poly)
    db.commit()
    db.refresh(db_poly)

    return {
        "id": db_poly.id,
        "name": db_poly.name,
        "geom": mapping(to_shape(db_poly.geom))
    }


@router.get("/{polygon_id}", response_model=PolygonRead)
def read_polygon(polygon_id: int, db: Session = Depends(get_db)):
    polygon = db.query(Polygon).filter(Polygon.id == polygon_id).first()
    if not polygon:
        raise HTTPException(status_code=404, detail="Polygon not found")

    return {
        "id": polygon.id,
        "name": polygon.name,
        "geom": mapping(to_shape(polygon.geom))
    }

@router.get("/", response_model=list[PolygonRead])
def read_all_polygons(db: Session = Depends(get_db)):
    polygons = db.query(Polygon).all()
    return [
        {
            "id": poly.id,
            "name": poly.name,
            "geom": mapping(to_shape(poly.geom))
        }
        for poly in polygons
    ]

@router.put("/{polygon_id}", response_model=PolygonRead)
def update_polygon(polygon_id: int, updated: PolygonCreate, db: Session = Depends(get_db)):
    polygon = db.query(Polygon).filter(Polygon.id == polygon_id).first()
    if not polygon:
        raise HTTPException(status_code=404, detail="Polygon not found")

    polygon.name = updated.name
    polygon.geom = from_shape(shape(updated.geom), srid=4326)
    db.commit()
    db.refresh(polygon)

    return {
        "id": polygon.id,
        "name": polygon.name,
        "geom": mapping(to_shape(polygon.geom))
    }


@router.get("/contains-point/{point_id}", response_model=list[PolygonRead])
def get_polygons_containing_point(point_id: int, db: Session = Depends(get_db)):
    from app.models.point import Point as PointModel

    point = db.query(PointModel).filter(PointModel.id == point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")

    polygons = db.query(Polygon).filter(
        func.ST_Contains(Polygon.geom, point.geom)
    ).all()

    return [
        {
            "id": poly.id,
            "name": poly.name,
            "geom": mapping(to_shape(poly.geom))
        }
        for poly in polygons
    ]


@router.delete("/wipe", tags=["Dev Utilities"])
def delete_all_polygons(db: Session = Depends(get_db)):
    db.query(Polygon).delete()
    db.commit()
    return {"message": "All polygons deleted"}
