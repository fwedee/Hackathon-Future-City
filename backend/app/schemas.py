from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WorkerBase(BaseModel):
    worker_id: str
    # Add other worker fields if necessary, for now we just need the ID to link

    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    item_name: str
    item_description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    item_id: str
    fk_branch_id: Optional[str] = None

    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    role_name: str
    role_description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    role_id: str

    class Config:
        from_attributes = True

class JobBase(BaseModel):
    job_name: Optional[str] = None
    job_description: Optional[str] = None
    longitude: float
    latitude: float
    country: Optional[str] = None
    city: Optional[str] = None
    house_number: Optional[str] = None
    street: Optional[str] = None
    postal_code: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

class JobItemLinkBase(BaseModel):
    item_id: str
    required_quantity: int = 1

class JobItemLinkCreate(JobItemLinkBase):
    pass

class JobItemLink(JobItemLinkBase):
    item: Item

    class Config:
        from_attributes = True

class JobCreate(JobBase):
    worker_ids: List[str] = []
    items: List[JobItemLinkCreate] = []
    role_ids: List[str] = []

class Job(JobBase):
    job_id: str
    workers: List[WorkerBase] = []
    item_links: List[JobItemLink] = []
    roles: List[Role] = []

    class Config:
        from_attributes = True
