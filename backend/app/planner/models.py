from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Branch:
    """Branch/depot location."""
    branch_id: str
    latitude: float
    longitude: float


@dataclass
class Worker:
    """Worker with their home branch and roles."""
    worker_id: str
    branch_id: str
    latitude: float  # from branch
    longitude: float  # from branch
    roles: List[str]  # list of role_ids this worker has


@dataclass
class Stock:
    """Stock item at a branch."""
    stock_id: str
    item_id: str
    branch_id: str
    latitude: float  # from branch
    longitude: float  # from branch
    quantity: int  # available quantity


@dataclass
class Job:
    """Job with requirements."""
    job_id: str
    latitude: float
    longitude: float
    start_datetime: datetime
    end_datetime: datetime
    required_roles: Dict[str, int]  # {role_id: quantity}
    required_items: Dict[str, int]  # {item_id: quantity}


@dataclass
class PlannerInput:
    """Complete input data for the planner."""
    jobs: List[Job]
    workers: List[Worker]
    stocks: List[Stock]
    branches: List[Branch]
