from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal, engine, Base
from app.models import models
from app import schemas

# Create tables
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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

# Workers
@app.get("/workers", response_model=List[schemas.WorkerBase])
def read_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workers = db.query(models.Worker).offset(skip).limit(limit).all()
    return workers

# Items
@app.get("/items", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

@app.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict()) 
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Roles
@app.get("/roles", response_model=List[schemas.Role])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = db.query(models.Role).offset(skip).limit(limit).all()
    return roles

@app.post("/roles", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Jobs
@app.post("/jobs", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = models.Job(
        longitude=job.longitude,
        latitude=job.latitude,
        country=job.country,
        city=job.city,
        house_number=job.house_number,
        street=job.street,
        postal_code=job.postal_code,
        start_datetime=job.start_datetime,
        end_datetime=job.end_datetime
    )
    
    # Handle workers
    if job.worker_ids:
        workers = db.query(models.Worker).filter(models.Worker.worker_id.in_(job.worker_ids)).all()
        db_job.workers = workers
        
    # Handle items
    if job.item_ids:
        items = db.query(models.Item).filter(models.Item.item_id.in_(job.item_ids)).all()
        db_job.items = items

    # Handle roles
    if job.role_ids:
        roles = db.query(models.Role).filter(models.Role.role_id.in_(job.role_ids)).all()
        db_job.roles = roles

    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(models.Job).offset(skip).limit(limit).all()
    return jobs

@app.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: str, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.job_id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.put("/jobs/{job_id}", response_model=schemas.Job)
def update_job(job_id: str, job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.job_id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update basic fields
    job_data = job.dict(exclude={'worker_ids', 'item_ids', 'role_ids'})
    for key, value in job_data.items():
        setattr(db_job, key, value)
    
    # Update relationships
    if job.worker_ids is not None:
        workers = db.query(models.Worker).filter(models.Worker.worker_id.in_(job.worker_ids)).all()
        db_job.workers = workers
        
    if job.item_ids is not None:
        items = db.query(models.Item).filter(models.Item.item_id.in_(job.item_ids)).all()
        db_job.items = items

    if job.role_ids is not None:
        roles = db.query(models.Role).filter(models.Role.role_id.in_(job.role_ids)).all()
        db_job.roles = roles
        
    db.commit()
    db.refresh(db_job)
    return db_job

@app.delete("/jobs/{job_id}")
def delete_job(job_id: str, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.job_id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(db_job)
    db.commit()
    return {"message": "Job deleted successfully"}

