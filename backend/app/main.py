import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
import app.models.models  # Import models to register them with Base

# Check if database exists, if not initialize and seed it
DB_PATH = Path(__file__).parent.parent / "hackathon.db"
if not DB_PATH.exists():
    print("Database not found. Initializing database...")
    from seed.seed import seed_database
    Base.metadata.create_all(bind=engine)
    print("Database tables created. Seeding data...")
    seed_database()
    print("Database initialization complete!")
else:
    # Ensure tables exist (in case schema changed)
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
from app.routers import jobs as jobs_router
from app.routers import workers as workers_router
from app.routers import items as items_router
from app.routers import roles as roles_router
from app.routers import planner_test as planner_test_router # for testing planner

app.include_router(jobs_router.router)
app.include_router(workers_router.router)
app.include_router(items_router.router)
app.include_router(roles_router.router)
app.include_router(planner_test_router.router) # for testing planner
