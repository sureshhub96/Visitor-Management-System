from fastapi import FastAPI

from app.database import Base, engine

from app.routers.auth_router import router as auth_router
from app.routers.visitor_router import router as visitor_router
from app.routers.visit_router import router as visit_router


# Create all database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Visitor Management System",
    description="Visitor Management System using FastAPI",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Visitor Management System API"
    }


# Include Routers
app.include_router(auth_router)
app.include_router(visitor_router)
app.include_router(visit_router)