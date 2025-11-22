import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())

worker_job = Table(
    "worker__job",
    Base.metadata,
    Column("worker_id", String(36), ForeignKey("worker.worker_id"), primary_key=True),
    Column("job_id", String(36), ForeignKey("job.job_id"), primary_key=True),
)

item_job = Table(
    "item__job",
    Base.metadata,
    Column("item_id", String(36), ForeignKey("item.item_id"), primary_key=True),
    Column("job_id", String(36), ForeignKey("job.job_id"), primary_key=True),
)

job_role = Table(
    "job__role",
    Base.metadata,
    Column("job_id", String(36), ForeignKey("job.job_id"), primary_key=True),
    Column("role_id", String(36), ForeignKey("role.role_id"), primary_key=True),
)

class Branch(Base):
    __tablename__ = "branch"

    branch_id = Column(String(36), primary_key=True, default=generate_uuid)
    longitude = Column(Float)
    latitude = Column(Float)
    country = Column(String)
    city = Column(String)
    house_number = Column(String)
    street = Column(String)
    postal_code = Column(String)

    workers = relationship("Worker", back_populates="branch")
    items = relationship("Item", back_populates="branch")


class Worker(Base):
    __tablename__ = "worker"

    worker_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String, nullable=True)
    fk_branch_id = Column(String(36), ForeignKey("branch.branch_id"))

    branch = relationship("Branch", back_populates="workers")
    jobs = relationship("Job", secondary=worker_job, back_populates="workers")


class Item(Base):
    __tablename__ = "item"

    item_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    fk_branch_id = Column(String(36), ForeignKey("branch.branch_id"))

    branch = relationship("Branch", back_populates="items")
    jobs = relationship("Job", secondary=item_job, back_populates="items")


class Role(Base):
    __tablename__ = "role"

    role_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)

    jobs = relationship("Job", secondary=job_role, back_populates="roles")


class Job(Base):
    __tablename__ = "job"

    job_id = Column(String(36), primary_key=True, default=generate_uuid)
    longitude = Column(Float)
    latitude = Column(Float)
    country = Column(String)
    city = Column(String)
    house_number = Column(String)
    street = Column(String)
    postal_code = Column(String)
    start_datetime = Column(DateTime, nullable=True)
    end_datetime = Column(DateTime, nullable=True)

    workers = relationship("Worker", secondary=worker_job, back_populates="jobs")
    items = relationship("Item", secondary=item_job, back_populates="jobs")
    roles = relationship("Role", secondary=job_role, back_populates="jobs")
