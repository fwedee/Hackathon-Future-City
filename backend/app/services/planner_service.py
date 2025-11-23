"""Service layer for running the planner and updating database."""
from typing import Dict, List
from sqlalchemy.orm import Session
from datetime import datetime
import threading

from app.models.models import (
    Job, Worker, Branch, Stock, Item, Role,
    worker__job, job__stock, worker__role
)
from app.planner.planner import compute_plan, format_for_database
from app.planner.models import (
    PlannerInput,
    Job as PlannerJob,
    Worker as PlannerWorker,
    Stock as PlannerStock,
    Branch as PlannerBranch
)
from app.core.database import SessionLocal


def _run_planner_internal(max_time_seconds: float = 30.0, debug: bool = False) -> Dict:
    """
    Internal function that runs the planner with its own database session.
    Used by background thread.
    """
    db = SessionLocal()
    try:
        return _execute_planner(db, max_time_seconds, debug)
    finally:
        db.close()


def fetch_and_run_planner(db: Session, max_time_seconds: float = 30.0, debug: bool = False) -> Dict:
    """
    Fetch all data from database, run planner, and update assignments.
    
    Steps:
    1. Fetch all workers, branches, items, stocks, jobs from DB
    2. Convert to planner format
    3. Run planner
    4. Update worker__job and job__stock tables with results
    
    Args:
        db: Database session
        max_time_seconds: Max solver time
        debug: If True, print detailed logs to console
    
    Returns:
        Planner result dictionary
    """
    return _execute_planner(db, max_time_seconds, debug)


def fetch_and_run_planner_async(max_time_seconds: float = 30.0, debug: bool = False) -> Dict:
    """
    Run planner in background thread and return immediately.
    
    This function starts the planner in a daemon thread and returns immediately
    without waiting for completion. Useful for API endpoints that need to respond quickly.
    
    Args:
        max_time_seconds: Max solver time
        debug: If True, print detailed logs to console
    
    Returns:
        Status dictionary indicating the planner was started
    """
    # Start planner in background thread
    thread = threading.Thread(
        target=_run_planner_internal,
        args=(max_time_seconds, debug),
        daemon=True
    )
    thread.start()
    
    return {
        "status": "STARTED",
        "message": "Planner started in background",
        "thread_id": thread.ident
    }


def _execute_planner(db: Session, max_time_seconds: float, debug: bool) -> Dict:
    """
    Core planner execution logic.
    
    Args:
        db: Database session
        max_time_seconds: Max solver time
        debug: If True, print detailed logs to console
    
    Returns:
        Planner result dictionary
    """
    start_time = datetime.now()
    if debug:
        print(f"\n{'='*60}")
        print(f"[PLANNER SERVICE] Started at {start_time.strftime('%H:%M:%S.%f')[:-3]}")
        print(f"{'='*60}")
    
    # === Step 1: Fetch all data ===
    if debug:
        print("[STEP 1] Fetching data from database...")
    
    db_branches = db.query(Branch).all()
    db_workers = db.query(Worker).all()
    db_stocks = db.query(Stock).all()
    db_jobs = db.query(Job).all()
    db_roles = db.query(Role).all()
    
    if debug:
        print(f"  → Fetched {len(db_jobs)} jobs, {len(db_workers)} workers, {len(db_stocks)} stocks, {len(db_branches)} branches")
    
    if not db_jobs:
        if debug:
            print("[WARNING] No jobs to plan. Exiting.")
        return {
            "status": "NO_JOBS",
            "message": "No jobs to plan",
            "jobs": {}
        }
    
    # === Step 2: Convert to planner format ===
    if debug:
        print("[STEP 2] Converting data to planner format...")
    
    # Build branch lookup
    branch_map = {b.branch_id: b for b in db_branches}
    
    # Build role lookup (role_id -> role_name)
    role_map = {r.role_id: r.role_name for r in db_roles}
    
    # Convert branches
    planner_branches = [
        PlannerBranch(
            branch_id=b.branch_id,
            latitude=b.latitude or 0.0,
            longitude=b.longitude or 0.0
        )
        for b in db_branches
    ]
    
    # Convert workers
    planner_workers = []
    for w in db_workers:
        branch = branch_map.get(w.fk_branch_id)
        if not branch:
            continue
        
        # Get worker's role names from worker__role table
        worker_role_ids = [
            wr.role_id for wr in 
            db.execute(worker__role.select().where(worker__role.c.worker_id == w.worker_id))
        ]
        worker_role_names = [role_map.get(rid, "") for rid in worker_role_ids if rid in role_map]
        
        planner_workers.append(
            PlannerWorker(
                worker_id=w.worker_id,
                branch_id=w.fk_branch_id,
                latitude=branch.latitude or 0.0,
                longitude=branch.longitude or 0.0,
                roles=worker_role_names
            )
        )
    
    # Convert stocks
    planner_stocks = []
    for s in db_stocks:
        branch = branch_map.get(s.fk_branch_id)
        if not branch:
            continue
        
        planner_stocks.append(
            PlannerStock(
                stock_id=s.stock_id,
                item_id=s.fk_item_id,
                branch_id=s.fk_branch_id,
                latitude=branch.latitude or 0.0,
                longitude=branch.longitude or 0.0,
                quantity=s.quantity
            )
        )
    
    # Convert jobs
    planner_jobs = []
    for j in db_jobs:
        # Get required roles from job__role table
        required_roles = {}
        job_roles = db.execute(
            db.query(Role.role_id, Role.role_name)
            .join(Job.roles)
            .filter(Job.job_id == j.job_id)
        ).all()
        for role_id, role_name in job_roles:
            required_roles[role_name] = required_roles.get(role_name, 0) + 1
        
        # Get required items from job__item table
        required_items = {}
        for item_link in j.item_links:
            item_id = item_link.item_id
            quantity = item_link.required_quantity or 0
            required_items[item_id] = required_items.get(item_id, 0) + quantity
        
        planner_jobs.append(
            PlannerJob(
                job_id=j.job_id,
                latitude=j.latitude or 0.0,
                longitude=j.longitude or 0.0,
                start_datetime=j.start_datetime,
                end_datetime=j.end_datetime,
                required_roles=required_roles,
                required_items=required_items
            )
        )
    
    # Create planner input
    planner_input = PlannerInput(
        jobs=planner_jobs,
        workers=planner_workers,
        stocks=planner_stocks,
        branches=planner_branches
    )
    
    if debug:
        print(f"  → Converted {len(planner_jobs)} jobs, {len(planner_workers)} workers, {len(planner_stocks)} stocks")
    
    # === Step 3: Run planner ===
    if debug:
        print(f"[STEP 3] Running OR-Tools CP-SAT solver (max {max_time_seconds}s)...")
    planner_start_time = datetime.now()
    
    result = compute_plan(planner_input, max_time_seconds=max_time_seconds)
    
    planner_end_time = datetime.now()
    solver_duration = (planner_end_time - planner_start_time).total_seconds()
    if debug:
        print(f"  → Solver completed in {solver_duration:.2f}s")
        print(f"  → Status: {result.get('status')}")
        print(f"  → Jobs assigned: {len([j for j in result.get('jobs', {}).values() if j.get('workers')])}/{len(planner_jobs)}")
    
    # === Step 4: Update database tables ===
    if debug:
        print("[STEP 4] Updating database tables...")
    
    # Clear existing assignments (for all jobs)
    job_ids = [j.job_id for j in db_jobs]
    db.execute(worker__job.delete().where(worker__job.c.job_id.in_(job_ids)))
    db.execute(job__stock.delete().where(job__stock.c.job_id.in_(job_ids)))
    
    # Insert new assignments
    worker_job_records, job_stock_records = format_for_database(result)
    
    if worker_job_records:
        db.execute(worker__job.insert(), worker_job_records)
    
    if job_stock_records:
        db.execute(job__stock.insert(), job_stock_records)
    
    db.commit()
    
    if debug:
        print(f"  → Inserted {len(worker_job_records)} worker assignments")
        print(f"  → Inserted {len(job_stock_records)} stock assignments")
    
    end_time = datetime.now()
    total_duration = (end_time - start_time).total_seconds()
    if debug:
        print(f"{'='*60}")
        print(f"[PLANNER SERVICE] Completed in {total_duration:.2f}s")
        print(f"{'='*60}\n")
    
    return result
