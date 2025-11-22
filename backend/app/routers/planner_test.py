"""Test route for the planner with sample data."""
from datetime import datetime, timedelta
from fastapi import APIRouter

from app.planner.planner import compute_plan, format_for_database
from app.planner.models import PlannerInput, Job, Worker, Stock, Branch

router = APIRouter()


@router.get("/planner/test", tags=["planner"])
def test_planner():
    """
    Test endpoint that generates sample data and runs the planner.
    No input required - uses hardcoded test data.
    """
    
    # Sample branches
    branches = [
        Branch(
            branch_id="branch_1",
            latitude=52.5200,  # Berlin
            longitude=13.4050
        ),
        Branch(
            branch_id="branch_2",
            latitude=52.3759,  # Potsdam
            longitude=13.0622
        ),
        Branch(
            branch_id="branch_3",
            latitude=52.4537,  # Brandenburg
            longitude=12.5510
        )
    ]
    
    # Sample workers with roles
    workers = [
        Worker(
            worker_id="worker_1",
            branch_id="branch_1",
            latitude=52.5200,
            longitude=13.4050,
            roles=["electrician", "general"]
        ),
        Worker(
            worker_id="worker_2",
            branch_id="branch_1",
            latitude=52.5200,
            longitude=13.4050,
            roles=["plumber", "general"]
        ),
        Worker(
            worker_id="worker_3",
            branch_id="branch_2",
            latitude=52.3759,
            longitude=13.0622,
            roles=["electrician", "plumber"]
        ),
        Worker(
            worker_id="worker_4",
            branch_id="branch_2",
            latitude=52.3759,
            longitude=13.0622,
            roles=["general"]
        ),
        Worker(
            worker_id="worker_5",
            branch_id="branch_3",
            latitude=52.4537,
            longitude=12.5510,
            roles=["electrician"]
        )
    ]
    
    # Sample stocks
    stocks = [
        Stock(
            stock_id="stock_1",
            item_id="item_cables",
            branch_id="branch_1",
            latitude=52.5200,
            longitude=13.4050,
            quantity=50
        ),
        Stock(
            stock_id="stock_2",
            item_id="item_pipes",
            branch_id="branch_1",
            latitude=52.5200,
            longitude=13.4050,
            quantity=30
        ),
        Stock(
            stock_id="stock_3",
            item_id="item_cables",
            branch_id="branch_2",
            latitude=52.3759,
            longitude=13.0622,
            quantity=40
        ),
        Stock(
            stock_id="stock_4",
            item_id="item_tools",
            branch_id="branch_2",
            latitude=52.3759,
            longitude=13.0622,
            quantity=20
        ),
        Stock(
            stock_id="stock_5",
            item_id="item_pipes",
            branch_id="branch_3",
            latitude=52.4537,
            longitude=12.5510,
            quantity=25
        )
    ]
    
    # Sample jobs
    today = datetime.now()
    jobs = [
        Job(
            job_id="job_1",
            latitude=52.5100,  # Central Berlin
            longitude=13.3900,
            start_datetime=today + timedelta(hours=1),
            end_datetime=today + timedelta(hours=4),
            required_roles={"electrician": 1, "general": 1},
            required_items={"item_cables": 10, "item_tools": 2}
        ),
        Job(
            job_id="job_2",
            latitude=52.3900,  # Near Potsdam
            longitude=13.0800,
            start_datetime=today + timedelta(hours=2),
            end_datetime=today + timedelta(hours=5),
            required_roles={"plumber": 1},
            required_items={"item_pipes": 8}
        ),
        Job(
            job_id="job_3",
            latitude=52.4800,  # Between Berlin and Brandenburg
            longitude=13.2500,
            start_datetime=today + timedelta(hours=5),
            end_datetime=today + timedelta(hours=7),
            required_roles={"electrician": 2},
            required_items={"item_cables": 15}
        ),
        Job(
            job_id="job_4",
            latitude=52.5300,  # North Berlin
            longitude=13.4200,
            start_datetime=today + timedelta(hours=1),
            end_datetime=today + timedelta(hours=3),
            required_roles={"general": 1},
            required_items={"item_tools": 1}
        )
    ]
    
    # Create planner input
    planner_input = PlannerInput(
        jobs=jobs,
        workers=workers,
        stocks=stocks,
        branches=branches
    )
    
    # Run planner
    result = compute_plan(planner_input, max_time_seconds=10.0)
    
    # Format for database
    worker_job_records, job_stock_records = format_for_database(result)
    
    # Return comprehensive result
    return {
        "planner_result": result,
        "database_format": {
            "worker_job_records": worker_job_records,
            "job_stock_records": job_stock_records
        },
        "summary": {
            "total_jobs": len(jobs),
            "total_workers": len(workers),
            "total_stocks": len(stocks),
            "total_branches": len(branches),
            "jobs_assigned": len([j for j in result.get("jobs", {}).values() if j.get("workers")]),
            "total_worker_assignments": len(worker_job_records),
            "total_stock_assignments": len(job_stock_records)
        }
    }
