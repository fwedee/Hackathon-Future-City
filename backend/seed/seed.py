from app.core.database import SessionLocal
from app.services.planner_service import fetch_and_run_planner

# Import seed functions
from seed.branches_seed import seed_branches
from seed.roles_seed import seed_roles
from seed.workers_seed import seed_workers
from seed.items_seed import seed_items
from seed.stocks_seed import seed_stocks
from seed.jobs_seed import seed_jobs, seed_job_items


def seed_database():
    """Seed all tables with initial data in correct dependency order"""
    db = SessionLocal()
    
    try:
        print("Starting database seeding...")
        
        # 1. Seed independent tables first (no foreign keys)
        print("Seeding branches...")
        branches = seed_branches()
        for branch in branches:
            db.add(branch)
        db.flush()
        print(f"  ✓ {len(branches)} branches created")
        
        print("Seeding roles...")
        roles = seed_roles()
        for role in roles:
            db.add(role)
        db.flush()
        print(f"  ✓ {len(roles)} roles created")
        
        # 2. Seed tables that depend on branches and roles
        print("Seeding workers...")
        workers = seed_workers(branches, roles)
        for worker in workers:
            db.add(worker)
        db.flush()
        print(f"  ✓ {len(workers)} workers created with role assignments")
        
        print("Seeding items...")
        items = seed_items(branches)
        for item in items:
            db.add(item)
        db.flush()
        print(f"  ✓ {len(items)} items created")
        
        # 3. Seed stock (depends on branches and items)
        print("Seeding stocks...")
        stocks = seed_stocks(branches, items)
        for stock in stocks:
            db.add(stock)
        db.flush()
        print(f"  ✓ {len(stocks)} stock entries created")
        
        # 4. Seed jobs (depends on roles)
        print("Seeding jobs...")
        jobs, job_items_list = seed_jobs(roles)
        for job in jobs:
            db.add(job)
        db.flush()
        print(f"  ✓ {len(jobs)} jobs created with role requirements")
        
        # 5. Seed job-item associations (depends on jobs and items)
        print("Seeding job-item associations...")
        job_items = seed_job_items(jobs, items, job_items_list)
        for job_item in job_items:
            db.add(job_item)
        db.flush()
        print(f"  ✓ {len(job_items)} job-item associations created")
        
        db.commit()
        print("\n" + "="*60)
        print("Database seeding completed successfully!")
        print("="*60)
        print(f"Summary:")
        print(f"  - {len(branches)} branches")
        print(f"  - {len(roles)} roles")
        print(f"  - {len(workers)} workers")
        print(f"  - {len(items)} items")
        print(f"  - {len(stocks)} stock entries")
        print(f"  - {len(jobs)} jobs")
        print(f"  - {len(job_items)} job-item associations")
        print("="*60)
        
        # 6. Run planner to assign workers to jobs
        print("\nRunning planner to assign workers to jobs...")
        fetch_and_run_planner(db, debug=True)
        print("Planner completed successfully!")
        
    except Exception as e:
        print(f"\nError seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
