from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.models import Job, Item, Worker, Role, JobItem
from app import schemas
from app.services.planner_service import fetch_and_run_planner_async

router = APIRouter()

@router.post("/jobs", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = Job(
        job_name=job.job_name,
        job_description=job.job_description,
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
        workers = db.query(Worker).filter(Worker.worker_id.in_(job.worker_ids)).all()
        db_job.workers = workers
        
    # Handle items (with quantities)
    if job.items:
        for item_link in job.items:
            db_item_link = JobItem(item_id=item_link.item_id, required_quantity=item_link.required_quantity)
            db_job.item_links.append(db_item_link)

    # Handle roles
    if job.role_ids:
        roles = db.query(Role).filter(Role.role_id.in_(job.role_ids)).all()
        db_job.roles = roles

    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Run planner to update assignments (async, returns immediately)
    try:
        fetch_and_run_planner_async(debug=True)
    except Exception as e:
        # Log error but don't fail job creation
        print(f"Planner error: {e}")
    
    # Reload with eager loading to populate item_links.item
    db_job = db.query(Job).options(joinedload(Job.item_links).joinedload(JobItem.item)).filter(Job.job_id == db_job.job_id).first()
    return db_job

@router.get("/jobs", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(Job).options(joinedload(Job.item_links).joinedload(JobItem.item)).offset(skip).limit(limit).all()
    return jobs

@router.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: str, db: Session = Depends(get_db)):
    db_job = db.query(Job).options(joinedload(Job.item_links).joinedload(JobItem.item)).filter(Job.job_id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@router.put("/jobs/{job_id}", response_model=schemas.Job)
def update_job(job_id: str, job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.job_id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update basic fields
    job_data = job.dict(exclude={'worker_ids', 'items', 'role_ids'})
    for key, value in job_data.items():
        setattr(db_job, key, value)
    
    # Update relationships
    if job.worker_ids is not None:
        workers = db.query(Worker).filter(Worker.worker_id.in_(job.worker_ids)).all()
        db_job.workers = workers
        
    if job.items is not None:
        # Clear existing links and add new ones
        # Because of cascade="all, delete-orphan", removing from list deletes the association object
        db_job.item_links = []
        for item_link in job.items:
            db_item_link = JobItem(item_id=item_link.item_id, required_quantity=item_link.required_quantity)
            db_job.item_links.append(db_item_link)

    if job.role_ids is not None:
        roles = db.query(Role).filter(Role.role_id.in_(job.role_ids)).all()
        db_job.roles = roles
        
    db.commit()
    db.refresh(db_job)
    
    # Run planner to update assignments (async, returns immediately)
    try:
        fetch_and_run_planner_async(debug=True)
    except Exception as e:
        # Log error but don't fail job update
        print(f"Planner error: {e}")
    
    # Reload with eager loading to populate item_links.item
    db_job = db.query(Job).options(joinedload(Job.item_links).joinedload(JobItem.item)).filter(Job.job_id == job_id).first()
    return db_job

@router.delete("/jobs/{job_id}")
def delete_job(job_id: str, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.job_id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(db_job)
    db.commit()
    
    # Run planner to update assignments for remaining jobs (async, returns immediately)
    try:
        fetch_and_run_planner_async(debug=True)
    except Exception as e:
        # Log error but don't fail job deletion
        print(f"Planner error: {e}")
    
    return {"message": "Job deleted successfully"}

@router.get("/worker/{worker_id}/jobs", response_model=List[schemas.Job])
def get_jobs_by_worker_id(worker_id: str, db: Session = Depends(get_db)):
    # Verify worker exists
    worker = db.query(Worker).filter(Worker.worker_id == worker_id).first()
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Get all jobs assigned to this worker via worker__job table
    jobs = db.query(Job).join(Job.workers).filter(Worker.worker_id == worker_id).options(
        joinedload(Job.item_links).joinedload(JobItem.item),
        joinedload(Job.workers),
        joinedload(Job.roles)
    ).all()
    
    return jobs

