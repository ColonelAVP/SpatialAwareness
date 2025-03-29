Spatial Awareness - Spatial Data Platform Backend
Spatial Awareness is a geospatial data platform built using FastAPI and PostGIS, designed to handle point and polygon spatial data. It provides powerful REST APIs to perform spatial operations such as containment and proximity queries.

🚀 Features
CRUD APIs for:


Multiple Points (e.g., farm plots, sensors, dealers)


Multiple Polygons (e.g., geofences, zones)


Spatial queries:


✅ Get all points within a polygon


✅ Get all polygons containing a point


✅ Get all points within a radius (proximity search)


Swagger documentation for easy testing


Dockerized setup with persistent PostGIS database



🌍 Real-World Scenarios Demonstrated
🛡️ HAL Zone Defense Check
Polygon: HAL Zone (Defense area)


Points: 3 farm plots


Objective: Check whether any farm encroaches on the restricted zone using ST_Contains


🏪 Jayanagar 4th Block Market Optimization
Polygon: Market zone


Points: 4 vegetable bulk dealers


Objective: Help vendors choose the nearest dealer using ST_DWithin and visualize dealer locations inside the market boundary



🔧 Tech Stack
Python 3.10


FastAPI


PostgreSQL + PostGIS


SQLAlchemy + GeoAlchemy2


Docker & Docker Compose



🧪 API Endpoints
📍 Points
POST /points/ — Create point


GET /points/ — List all points


GET /points/{id} — Get point by ID


PUT /points/{id} — Update point


DELETE /points/wipe — Delete all (dev-only)


GET /points/within-polygon/{polygon_id} — Points inside polygon


GET /points/nearby?lat=...&lng=...&radius=... — Points within radius


🟦 Polygons
POST /polygons/ — Create polygon


GET /polygons/ — List all polygons


GET /polygons/{id} — Get polygon by ID


PUT /polygons/{id} — Update polygon


DELETE /polygons/wipe — Delete all (dev-only)


GET /polygons/contains-point/{point_id} — Polygons containing point



🛠️ Setup (Docker)
Clone this repository


Run:


docker-compose up --build

Create tables (run inside container):


docker exec -it spatial_awareness_web_1 bash
python
>>> from app.db import Base, engine
>>> import app.models.point, app.models.polygon
>>> Base.metadata.create_all(bind=engine)
>>> exit()

Visit Swagger: http://localhost:8000/docs



📽️ Demo
A product video demo has been recorded to walk through the features and real-world use cases clearly. You are encouraged to watch the [demo](https://drive.google.com/file/d/1ooLJ8SU2YVetjZrFSQeOx8y3sTUG1vId/view?usp=drive_link) to get full context.


