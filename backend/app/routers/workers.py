from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.models import Worker
from app import schemas

router = APIRouter()

@router.get("/workers", response_model=List[schemas.WorkerBase], tags=["workers"])
def list_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workers = db.query(Worker).options(
        joinedload(Worker.branch),
        joinedload(Worker.roles)
    ).offset(skip).limit(limit).all()
    return workers


@router.get("/workers/{worker_id}", response_model=schemas.WorkerBase, tags=["workers"])
def get_worker(worker_id: str, db: Session = Depends(get_db)):
    w = db.query(Worker).options(
        joinedload(Worker.branch),
        joinedload(Worker.roles)
    ).filter(Worker.worker_id == worker_id).first()
    if not w:
        raise HTTPException(status_code=404, detail="Worker not found")
    return w
