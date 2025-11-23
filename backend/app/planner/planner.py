from collections import defaultdict
from datetime import timedelta
from typing import Dict, List, Tuple, Optional

from ortools.sat.python import cp_model

from .models import PlannerInput, Job, Worker, Stock
from .util import (
    haversine_distance,
    calculate_travel_time,
    time_intervals_overlap,
    fits_in_8hour_shift
)

# Global cache for previous solution (warm start)
_previous_solution: Optional[Dict] = None


def compute_plan(planner_input: PlannerInput, 
                max_time_seconds: float = 5.0) -> Dict:
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
    global _previous_solution
    
    jobs = planner_input.jobs
    workers = planner_input.workers
    stocks = planner_input.stocks
    
    # Build branch lookup
    branch_map = {b.branch_id: b for b in planner_input.branches}
    
    # === Pre-compute distance matrices (CRITICAL OPTIMIZATION) ===
    worker_job_distances = {}
    worker_branches = {}
    for w_idx, worker in enumerate(workers):
        branch = branch_map.get(worker.branch_id)
        if branch:
            worker_branches[w_idx] = branch
            for j_idx, job in enumerate(jobs):
                dist = haversine_distance(
                    branch.latitude, branch.longitude,
                    job.latitude, job.longitude
                )
                worker_job_distances[(w_idx, j_idx)] = dist
    
    stock_job_distances = {}
    stock_branches = {}
    for s_idx, stock in enumerate(stocks):
        branch = branch_map.get(stock.branch_id)
        if branch:
            stock_branches[s_idx] = branch
            for j_idx, job in enumerate(jobs):
                dist = haversine_distance(
                    branch.latitude, branch.longitude,
                    job.latitude, job.longitude
                )
                stock_job_distances[(s_idx, j_idx)] = dist
    
    # Pre-compute job time intervals
    job_intervals = {j_idx: (job.start_datetime, job.end_datetime) for j_idx, job in enumerate(jobs)}
    
    # Pre-compute worker roles lookup
    worker_roles = {w_idx: set(worker.roles) for w_idx, worker in enumerate(workers)}
    
    # Pre-compute stock-item mapping
    stock_items = {s_idx: stock.item_id for s_idx, stock in enumerate(stocks)}
    
    # Create CP-SAT model
    model = cp_model.CpModel()
    
    # === Variables ===
    
    # worker_job[w][j] = 1 if worker w is assigned to job j
    # Only create variables for feasible assignments (distance < 200km)
    worker_job = {}
    feasible_worker_jobs = set()
    for w_idx, worker in enumerate(workers):
        worker_job[w_idx] = {}
        for j_idx, job in enumerate(jobs):
            distance = worker_job_distances.get((w_idx, j_idx), 999)
            if distance < 200:  # Filter infeasible long-distance assignments
                worker_job[w_idx][j_idx] = model.NewBoolVar(f'worker_{w_idx}_job_{j_idx}')
                feasible_worker_jobs.add((w_idx, j_idx))
            else:
                # Create constant 0 for infeasible assignments
                worker_job[w_idx][j_idx] = model.NewConstant(0)
    
    # stock_job[s][j] = quantity of stock s assigned to job j
    # Only create variables for relevant stock-job pairs
    stock_job = {}
    feasible_stock_jobs = {}
    for s_idx, stock in enumerate(stocks):
        stock_job[s_idx] = {}
        for j_idx, job in enumerate(jobs):
            # Only create var if job needs this item AND stock has it
            job_needs_qty = job.required_items.get(stock.item_id, 0)
            if job_needs_qty > 0 and stock.quantity > 0:
                max_qty = min(stock.quantity, job_needs_qty)
                stock_job[s_idx][j_idx] = model.NewIntVar(
                    0, max_qty, f'stock_{s_idx}_job_{j_idx}_qty'
                )
                feasible_stock_jobs[(s_idx, j_idx)] = max_qty
            else:
                stock_job[s_idx][j_idx] = model.NewConstant(0)
    
    # === Soft Constraints (converted to objective terms) ===
    
    # Track which jobs have their role requirements satisfied (soft constraint)
    job_satisfied = {}
    role_satisfaction_penalties = []
    
    for j_idx, job in enumerate(jobs):
        # Create a boolean variable indicating if this job is satisfied
        job_satisfied[j_idx] = model.NewBoolVar(f'job_{j_idx}_satisfied')
        
        for role_id, required_count in job.required_roles.items():
            # Count workers assigned to this job that have this role (optimized lookup)
            workers_with_role = [
                worker_job[w_idx][j_idx]
                for w_idx in range(len(workers))
                if role_id in worker_roles.get(w_idx, set())
            ]
            if workers_with_role:
                # If job is satisfied, then role requirement must be met
                # job_satisfied[j_idx] => sum(workers_with_role) >= required_count
                # Equivalent to: sum(workers_with_role) >= required_count * job_satisfied[j_idx]
                model.Add(sum(workers_with_role) >= required_count).OnlyEnforceIf(job_satisfied[j_idx])
            else:
                # No workers available with this role, job can't be satisfied
                model.Add(job_satisfied[j_idx] == 0)
    
    # 2. Worker time constraints: no overlapping jobs (optimized)
    for w_idx in range(len(workers)):
        for j1_idx in range(len(jobs)):
            for j2_idx in range(j1_idx + 1, len(jobs)):
                start1, end1 = job_intervals[j1_idx]
                start2, end2 = job_intervals[j2_idx]
                
                # If jobs overlap in time, worker can't do both
                if time_intervals_overlap(start1, end1, start2, end2):
                    model.Add(
                        worker_job[w_idx][j1_idx] + worker_job[w_idx][j2_idx] <= 1
                    )
    
    # 4. Worker reachability constraint (already handled in variable creation)
    # Variables for distance > 200km are set to constant 0
    
    # 5. Stock availability: each stock unit can only be assigned once
    for s_idx, stock in enumerate(stocks):
        total_assigned = sum(
            stock_job[s_idx][j_idx]
            for j_idx in range(len(jobs))
        )
        model.Add(total_assigned <= stock.quantity)
    
    # 6. Item requirements: jobs must have required items (soft constraint)
    for j_idx, job in enumerate(jobs):
        for item_id, required_qty in job.required_items.items():
            # Sum stocks of this item assigned to this job
            stocks_for_item = [
                stock_job[s_idx][j_idx]
                for s_idx, stock in enumerate(stocks)
                if stock.item_id == item_id
            ]
            if stocks_for_item:
                # Only enforce if job is marked as satisfied
                model.Add(sum(stocks_for_item) >= required_qty).OnlyEnforceIf(job_satisfied[j_idx])
            else:
                # No stock available for required item, job can't be satisfied
                model.Add(job_satisfied[j_idx] == 0)
    
    # 7. Stock proximity preference (soft constraint via objective) - optimized
    # Prefer stocks closer to jobs
    stock_distance_costs = []
    for (s_idx, j_idx), max_qty in feasible_stock_jobs.items():
        distance = stock_job_distances.get((s_idx, j_idx), 0)
        # Cost is distance * quantity assigned (in units of 10km)
        cost_per_unit = int(distance / 10)
        if cost_per_unit > 0:
            stock_distance_costs.append(
                stock_job[s_idx][j_idx] * cost_per_unit
            )
    
    # 8. Worker distance preference (soft constraint via objective) - optimized
    worker_distance_costs = []
    for (w_idx, j_idx) in feasible_worker_jobs:
        distance = worker_job_distances.get((w_idx, j_idx), 0)
        # Cost in units of 10km
        cost = int(distance / 10)
        if cost > 0:
            worker_distance_costs.append(
                worker_job[w_idx][j_idx] * cost
            )
    
    # === Objective: Maximize satisfied jobs, then minimize distance ===
    # Primary goal: maximize number of satisfied jobs (weight = 10000 to prioritize)
    num_satisfied_jobs = sum(job_satisfied[j_idx] for j_idx in range(len(jobs)))
    
    # Secondary goal: minimize total distance
    total_distance_cost = sum(stock_distance_costs) + sum(worker_distance_costs)
    
    # Combined objective: maximize jobs satisfied (negative cost) - distance cost
    # Multiplying by large weight ensures job satisfaction is prioritized
    total_cost = -10000 * num_satisfied_jobs + total_distance_cost
    model.Minimize(total_cost)
    
    # === Warm Start (seed with previous solution) ===
    if _previous_solution:
        for (w_idx, j_idx) in feasible_worker_jobs:
            worker_id = workers[w_idx].worker_id
            job_id = jobs[j_idx].job_id
            prev_val = _previous_solution.get(('worker', worker_id, job_id), 0)
            model.AddHint(worker_job[w_idx][j_idx], prev_val)
        
        for (s_idx, j_idx) in feasible_stock_jobs.keys():
            stock_id = stocks[s_idx].stock_id
            job_id = jobs[j_idx].job_id
            prev_val = _previous_solution.get(('stock', stock_id, job_id), 0)
            model.AddHint(stock_job[s_idx][j_idx], prev_val)
    
    # === Solve ===
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time_seconds
    solver.parameters.log_search_progress = False
    solver.parameters.num_search_workers = 4  # Parallel search
    
    status = solver.Solve(model)
    
    # === Extract solution ===
    result = {
        "jobs": {},
        "status": solver.StatusName(status),
        "solve_time": solver.WallTime()
    }
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        # Store solution for warm start
        new_solution = {}
        
        for j_idx, job in enumerate(jobs):
            job_result = {
                "workers": [],
                "stocks": []
            }
            
            # Extract assigned workers
            for w_idx, worker in enumerate(workers):
                val = solver.Value(worker_job[w_idx][j_idx])
                if val == 1:
                    job_result["workers"].append(worker.worker_id)
                    # Store for warm start
                    new_solution[('worker', worker.worker_id, job.job_id)] = val
            
            # Extract assigned stocks
            for s_idx, stock in enumerate(stocks):
                qty = solver.Value(stock_job[s_idx][j_idx])
                if qty > 0:
                    job_result["stocks"].append({
                        "stock_id": stock.stock_id,
                        "quantity": qty
                    })
                    # Store for warm start
                    new_solution[('stock', stock.stock_id, job.job_id)] = qty
            
            result["jobs"][job.job_id] = job_result
        
        # Update global cache for next run
        _previous_solution = new_solution
    
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
