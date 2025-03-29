
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.point import PointCreate, PointRead
from app.models.point import Point
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


@router.post("/", response_model=PointRead)
def create_point(point: PointCreate, db: Session = Depends(get_db)):
    geom = from_shape(shape(point.geom), srid=4326)
    db_point = Point(name=point.name, geom=geom)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)

    result = {
        "id": db_point.id,
        "name": db_point.name,
        "geom": mapping(to_shape(db_point.geom))
    }
    return result



@router.get("/", response_model=list[PointRead])
def read_all_points(db: Session = Depends(get_db)):
    points = db.query(Point).all()
    return [
        {
            "id": point.id,
            "name": point.name,
            "geom": mapping(to_shape(point.geom))
        }
        for point in points
    ]

@router.put("/{point_id}", response_model=PointRead)
def update_point(point_id: int, updated: PointCreate, db: Session = Depends(get_db)):
    point = db.query(Point).filter(Point.id == point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")

    point.name = updated.name
    point.geom = from_shape(shape(updated.geom), srid=4326)
    db.commit()
    db.refresh(point)

    return {
        "id": point.id,
        "name": point.name,
        "geom": mapping(to_shape(point.geom))
    }


@router.get("/within-polygon/{polygon_id}", response_model=list[PointRead])
def get_points_within_polygon(polygon_id: int, db: Session = Depends(get_db)):
    from app.models.polygon import Polygon as PolygonModel

    polygon = db.query(PolygonModel).filter(PolygonModel.id == polygon_id).first()
    if not polygon:
        raise HTTPException(status_code=404, detail="Polygon not found")

    points = db.query(Point).filter(
        func.ST_Contains(polygon.geom, Point.geom)
    ).all()

    return [
        {
            "id": point.id,
            "name": point.name,
            "geom": mapping(to_shape(point.geom))
        }
        for point in points
    ]

@router.get("/nearby", response_model=list[PointRead])
def get_nearby_points(lat: float, lng: float, radius: float, db: Session = Depends(get_db)):
    center = func.ST_SetSRID(func.ST_Point(lng, lat), 4326)

    points = db.query(Point).filter(
        func.ST_DWithin(Point.geom, center, radius)
    ).all()

    return [
        {
            "id": point.id,
            "name": point.name,
            "geom": mapping(to_shape(point.geom))
        }
        for point in points
    ]


@router.get("/{point_id}", response_model=PointRead)
def read_point(point_id: int, db: Session = Depends(get_db)):
    point = db.query(Point).filter(Point.id == point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")

    return {
        "id": point.id,
        "name": point.name,
        "geom": mapping(to_shape(point.geom))
    }


@router.delete("/wipe", tags=["Dev Utilities"])
def delete_all_points(db: Session = Depends(get_db)):
    db.query(Point).delete()
    db.commit()
    return {"message": "All points deleted"}