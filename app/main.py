from fastapi import FastAPI
from app.routes import point_routes, polygon_routes

app = FastAPI(title="GeoSphere - Spatial Backend API")

app.include_router(point_routes.router, prefix="/points", tags=["Points"])
app.include_router(polygon_routes.router, prefix="/polygons", tags=["Polygons"])

@app.get("/")
def root():
    return {"message": "Hi, your spatial awareness mode is ON 🚀"}
