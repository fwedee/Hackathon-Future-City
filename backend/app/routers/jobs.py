from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Job
from app import schemas

router = APIRouter()

@router.post("/jobs", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = Job(
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

@router.get("/jobs", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(models.Job).offset(skip).limit(limit).all()
    return jobs

@router.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: str, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.job_id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@router.put("/jobs/{job_id}", response_model=schemas.Job)
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

@router.delete("/jobs/{job_id}")
def delete_job(job_id: str, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.job_id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(db_job)
    db.commit()
    return {"message": "Job deleted successfully"}

