import uuid
from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey,
    Table,
    DateTime,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


# Association tables (many-to-many)
worker__job = Table(
    "worker__job",
    Base.metadata,
    Column("worker_id", String(36), ForeignKey("worker.worker_id"), primary_key=True),
    Column("job_id", String(36), ForeignKey("job.job_id"), primary_key=True),
)

worker__role = Table(
    "worker__role",
    Base.metadata,
    Column("worker_id", String(36), ForeignKey("worker.worker_id"), primary_key=True),
    Column("role_id", String(36), ForeignKey("role.role_id"), primary_key=True),
)

job__role = Table(
    "job__role",
    Base.metadata,
    Column("job_id", String(36), ForeignKey("job.job_id"), primary_key=True),
    Column("role_id", String(36), ForeignKey("role.role_id"), primary_key=True),
    Column("required_quantity", Integer, nullable=True),
)


# Association object for job-item with quantity
class JobItem(Base):
    __tablename__ = "job__item"
    
    job_id = Column(String(36), ForeignKey("job.job_id"), primary_key=True)
    item_id = Column(String(36), ForeignKey("item.item_id"), primary_key=True)
    required_quantity = Column(Integer, nullable=True, default=1)
    
    # Relationships to parent objects
    job = relationship("Job", back_populates="item_links")
    item = relationship("Item")


job__stock = Table(
    "job__stock",
    Base.metadata,
    Column("job_id", String(36), ForeignKey("job.job_id"), primary_key=True),
    Column("stock_id", String(36), ForeignKey("stock.stock_id"), primary_key=True),
    Column("assigned_quantity", Integer, nullable=True),
)


class Branch(Base):
    __tablename__ = "branch"

    branch_id = Column(String(36), primary_key=True, default=generate_uuid)
    branch_name = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    street = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)

    workers = relationship("Worker", back_populates="branch")
    items = relationship("Item", back_populates="branch")
    stocks = relationship("Stock", back_populates="branch")


class Worker(Base):
    __tablename__ = "worker"

    worker_id = Column(String(36), primary_key=True, default=generate_uuid)
    worker_first_name = Column(String, nullable=True)
    worker_last_name = Column(String, nullable=True)
    worker_phone_number = Column(String, nullable=True)
    fk_branch_id = Column(String(36), ForeignKey("branch.branch_id"), nullable=True)

    branch = relationship("Branch", back_populates="workers")
    jobs = relationship("Job", secondary=worker__job, back_populates="workers")
    roles = relationship("Role", secondary=worker__role, back_populates="workers")


class Item(Base):
    __tablename__ = "item"

    item_id = Column(String(36), primary_key=True, default=generate_uuid)
    item_name = Column(String, nullable=True)
    item_description = Column(Text, nullable=True)
    fk_branch_id = Column(String(36), ForeignKey("branch.branch_id"), nullable=True)

    branch = relationship("Branch", back_populates="items")
    stocks = relationship("Stock", back_populates="item")


class Role(Base):
    __tablename__ = "role"

    role_id = Column(String(36), primary_key=True, default=generate_uuid)
    role_name = Column(String, nullable=True)
    role_description = Column(Text, nullable=True)

    workers = relationship("Worker", secondary=worker__role, back_populates="roles")
    jobs = relationship("Job", secondary=job__role, back_populates="roles")


class Job(Base):
    __tablename__ = "job"

    job_id = Column(String(36), primary_key=True, default=generate_uuid)
    job_name = Column(String, nullable=True)
    job_description = Column(Text, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    street = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    start_datetime = Column(DateTime, nullable=True)
    end_datetime = Column(DateTime, nullable=True)

    workers = relationship("Worker", secondary=worker__job, back_populates="jobs")
    item_links = relationship("JobItem", back_populates="job", cascade="all, delete-orphan")
    roles = relationship("Role", secondary=job__role, back_populates="jobs")
    stocks = relationship("Stock", secondary=job__stock, back_populates="jobs")


class Stock(Base):
    __tablename__ = "stock"

    stock_id = Column(String(36), primary_key=True, default=generate_uuid)
    quantity = Column(Integer, nullable=False, default=0)
    fk_branch_id = Column(String(36), ForeignKey("branch.branch_id"), nullable=False)
    fk_item_id = Column(String(36), ForeignKey("item.item_id"), nullable=False)

    branch = relationship("Branch", back_populates="stocks")
    item = relationship("Item", back_populates="stocks")
    jobs = relationship("Job", secondary=job__stock, back_populates="stocks")

