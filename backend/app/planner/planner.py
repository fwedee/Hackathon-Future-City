from collections import defaultdict
from datetime import timedelta
from typing import Dict, List, Tuple

from ortools.sat.python import cp_model

from .models import PlannerInput, Job, Worker, Stock
from .util import (
    haversine_distance,
    calculate_travel_time,
    time_intervals_overlap,
    fits_in_8hour_shift
)


def compute_plan(planner_input: PlannerInput, 
                max_time_seconds: float = 30.0) -> Dict:
    """
    Compute optimal worker and stock assignments to jobs using OR-Tools CP-SAT solver.
    
    Constraints:
    - Workers must have the required roles for a job
    - Workers can only work one job at a time (no overlapping schedules)
    - Workers must return to their branch within 8 hours
    - Workers must be able to reach the job in time
    - Stock items can only be assigned once (availability constraint)
    - Stock must have sufficient quantity for job requirements
    
    Args:
        planner_input: Input data containing jobs, workers, stocks, and branches
        max_time_seconds: Maximum solver time in seconds
    
    Returns:
        Dictionary with structure:
        {
            "jobs": {
                "job_id": {
                    "workers": ["worker_id1", "worker_id2", ...],
                    "stocks": [{"stock_id": "id", "quantity": num}, ...]
                }
            },
            "status": "OPTIMAL" | "FEASIBLE" | "INFEASIBLE",
            "solve_time": float
        }
    """
    jobs = planner_input.jobs
    workers = planner_input.workers
    stocks = planner_input.stocks
    
    # Build branch lookup
    branch_map = {b.branch_id: b for b in planner_input.branches}
    
    # Create CP-SAT model
    model = cp_model.CpModel()
    
    # === Variables ===
    
    # worker_job[w][j] = 1 if worker w is assigned to job j
    worker_job = {}
    for w_idx, worker in enumerate(workers):
        worker_job[w_idx] = {}
        for j_idx, job in enumerate(jobs):
            worker_job[w_idx][j_idx] = model.NewBoolVar(f'worker_{w_idx}_job_{j_idx}')
    
    # stock_job[s][j] = quantity of stock s assigned to job j
    stock_job = {}
    for s_idx, stock in enumerate(stocks):
        stock_job[s_idx] = {}
        for j_idx, job in enumerate(jobs):
            # Max quantity is either stock available or job requirement
            max_qty = min(
                stock.quantity,
                job.required_items.get(stock.item_id, 0)
            )
            if max_qty > 0:
                stock_job[s_idx][j_idx] = model.NewIntVar(
                    0, max_qty, f'stock_{s_idx}_job_{j_idx}_qty'
                )
            else:
                stock_job[s_idx][j_idx] = model.NewIntVar(0, 0, f'stock_{s_idx}_job_{j_idx}_qty')
    
    # === Constraints ===
    
    # 1. Role requirements: each job must have workers with required roles
    for j_idx, job in enumerate(jobs):
        for role_id, required_count in job.required_roles.items():
            # Count workers assigned to this job that have this role
            workers_with_role = [
                worker_job[w_idx][j_idx]
                for w_idx, worker in enumerate(workers)
                if role_id in worker.roles
            ]
            if workers_with_role:
                model.Add(sum(workers_with_role) >= required_count)
    
    # 2. Worker time constraints: no overlapping jobs
    for w_idx, worker in enumerate(workers):
        for j1_idx in range(len(jobs)):
            for j2_idx in range(j1_idx + 1, len(jobs)):
                job1 = jobs[j1_idx]
                job2 = jobs[j2_idx]
                
                # If jobs overlap in time, worker can't do both
                if time_intervals_overlap(
                    job1.start_datetime, job1.end_datetime,
                    job2.start_datetime, job2.end_datetime
                ):
                    model.Add(
                        worker_job[w_idx][j1_idx] + worker_job[w_idx][j2_idx] <= 1
                    )
    
    # 3. Worker 8-hour shift constraint
    for w_idx, worker in enumerate(workers):
        branch = branch_map.get(worker.branch_id)
        if not branch:
            continue
        
        for j_idx, job in enumerate(jobs):
            # Check if job fits in 8-hour shift with travel
            if not fits_in_8hour_shift(
                branch.latitude, branch.longitude,
                job.latitude, job.longitude,
                job.start_datetime, job.end_datetime
            ):
                # Constraint: cannot assign this worker to this job
                model.Add(worker_job[w_idx][j_idx] == 0)
    
    # 4. Worker reachability constraint
    for w_idx, worker in enumerate(workers):
        branch = branch_map.get(worker.branch_id)
        if not branch:
            continue
        
        for j_idx, job in enumerate(jobs):
            # Assume worker starts from branch at shift start
            # Simple check: distance not too far for job start time
            distance = haversine_distance(
                branch.latitude, branch.longitude,
                job.latitude, job.longitude
            )
            # If distance > 200km, too far for typical daily assignment
            if distance > 200:
                model.Add(worker_job[w_idx][j_idx] == 0)
    
    # 5. Stock availability: each stock unit can only be assigned once
    for s_idx, stock in enumerate(stocks):
        total_assigned = sum(
            stock_job[s_idx][j_idx]
            for j_idx in range(len(jobs))
        )
        model.Add(total_assigned <= stock.quantity)
    
    # 6. Item requirements: jobs must have required items
    for j_idx, job in enumerate(jobs):
        for item_id, required_qty in job.required_items.items():
            # Sum stocks of this item assigned to this job
            stocks_for_item = [
                stock_job[s_idx][j_idx]
                for s_idx, stock in enumerate(stocks)
                if stock.item_id == item_id
            ]
            if stocks_for_item:
                model.Add(sum(stocks_for_item) >= required_qty)
    
    # 7. Stock proximity preference (soft constraint via objective)
    # Prefer stocks closer to jobs
    stock_distance_costs = []
    for s_idx, stock in enumerate(stocks):
        branch = branch_map.get(stock.branch_id)
        if not branch:
            continue
        
        for j_idx, job in enumerate(jobs):
            distance = haversine_distance(
                branch.latitude, branch.longitude,
                job.latitude, job.longitude
            )
            # Cost is distance * quantity assigned (in units of 10km)
            cost_per_unit = int(distance / 10)
            if cost_per_unit > 0:
                stock_distance_costs.append(
                    stock_job[s_idx][j_idx] * cost_per_unit
                )
    
    # 8. Worker distance preference (soft constraint via objective)
    worker_distance_costs = []
    for w_idx, worker in enumerate(workers):
        branch = branch_map.get(worker.branch_id)
        if not branch:
            continue
        
        for j_idx, job in enumerate(jobs):
            distance = haversine_distance(
                branch.latitude, branch.longitude,
                job.latitude, job.longitude
            )
            # Cost in units of 10km
            cost = int(distance / 10)
            if cost > 0:
                worker_distance_costs.append(
                    worker_job[w_idx][j_idx] * cost
                )
    
    # === Objective: Minimize total distance (prefer nearby assignments) ===
    total_cost = sum(stock_distance_costs) + sum(worker_distance_costs)
    model.Minimize(total_cost)
    
    # === Solve ===
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time_seconds
    solver.parameters.log_search_progress = False
    
    status = solver.Solve(model)
    
    # === Extract solution ===
    result = {
        "jobs": {},
        "status": solver.StatusName(status),
        "solve_time": solver.WallTime()
    }
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for j_idx, job in enumerate(jobs):
            job_result = {
                "workers": [],
                "stocks": []
            }
            
            # Extract assigned workers
            for w_idx, worker in enumerate(workers):
                if solver.Value(worker_job[w_idx][j_idx]) == 1:
                    job_result["workers"].append(worker.worker_id)
            
            # Extract assigned stocks
            for s_idx, stock in enumerate(stocks):
                qty = solver.Value(stock_job[s_idx][j_idx])
                if qty > 0:
                    job_result["stocks"].append({
                        "stock_id": stock.stock_id,
                        "quantity": qty
                    })
            
            result["jobs"][job.job_id] = job_result
    
    return result


def format_for_database(plan_result: Dict) -> Tuple[List[Dict], List[Dict]]:
    """
    Format planner result for database insertion.
    
    Args:
        plan_result: Result from compute_plan()
    
    Returns:
        Tuple of (worker_job_records, job_stock_records) ready for bulk insert
    """
    worker_job_records = []
    job_stock_records = []
    
    for job_id, assignments in plan_result.get("jobs", {}).items():
        # Worker-job associations
        for worker_id in assignments.get("workers", []):
            worker_job_records.append({
                "worker_id": worker_id,
                "job_id": job_id
            })
        
        # Job-stock associations
        for stock_assignment in assignments.get("stocks", []):
            job_stock_records.append({
                "job_id": job_id,
                "stock_id": stock_assignment["stock_id"],
                "assigned_quantity": stock_assignment["quantity"]
            })
    
    return worker_job_records, job_stock_records
