from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Item
from app import schemas

router = APIRouter()

@router.get("/items", response_model=List[schemas.Item], tags=["items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    
    result = []
    for item in items:
        total_stock = sum(stock.quantity for stock in item.stocks)
        item_data = schemas.Item.from_orm(item)
        item_data.total_stock = total_stock
        result.append(item_data)
        
    return result


@router.post("/items", response_model=schemas.Item, tags=["items"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/items/{item_id}", response_model=schemas.Item, tags=["items"])
def read_item(item_id: str, db: Session = Depends(get_db)):
    from app.models.models import JobItem
    
    db_item = db.query(Item).filter(Item.item_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Calculate total stock
    total_stock = sum(stock.quantity for stock in db_item.stocks)
    
    # Create a schema instance with the extra field
    item_data = schemas.Item.from_orm(db_item)
    item_data.total_stock = total_stock
    
    return item_data

@router.get("/item/{item_id}/jobs", response_model=List[schemas.Job], tags=["items"])
def read_jobs_by_item(item_id: str, db: Session = Depends(get_db)):
    from app.models.models import JobItem, Job
    
    # Check if item exists
    db_item = db.query(Item).filter(Item.item_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Get all jobs that use this item
    job_links = db.query(JobItem).filter(JobItem.item_id == item_id).all()
    job_ids = [link.job_id for link in job_links]
    
    jobs = db.query(Job).filter(Job.job_id.in_(job_ids)).all()
    
    return jobs

