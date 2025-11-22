import uuid
from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.models import models
from app.services.planner_service import fetch_and_run_planner


def seed_database():
    """Seed all tables with initial data"""
    db = SessionLocal()
    
    try:
        print("Starting database seeding...")
        
        # Seed Branches
        print("Seeding branches...")
        branches = [
            models.Branch(
                branch_id=str(uuid.uuid4()),
                branch_name="Berlin Central Warehouse",
                longitude=13.404954,
                latitude=52.520008,
                country="Germany",
                city="Berlin",
                street="Alexanderplatz",
                house_number="1",
                postal_code="10178"
            ),
            models.Branch(
                branch_id=str(uuid.uuid4()),
                branch_name="Potsdam Distribution Center",
                longitude=13.064473,
                latitude=52.390569,
                country="Germany",
                city="Potsdam",
                street="Brandenburger Straße",
                house_number="45",
                postal_code="14467"
            ),
            models.Branch(
                branch_id=str(uuid.uuid4()),
                branch_name="Brandenburg Logistics Hub",
                longitude=12.546284,
                latitude=52.412067,
                country="Germany",
                city="Brandenburg an der Havel",
                street="Hauptstraße",
                house_number="12",
                postal_code="14770"
            )
        ]
        for branch in branches:
            db.add(branch)
        db.flush()
        
        # Seed Roles
        print("Seeding roles...")
        roles = [
            models.Role(
                role_id=str(uuid.uuid4()),
                role_name="Electrician",
                role_description="Licensed electrician with certification"
            ),
            models.Role(
                role_id=str(uuid.uuid4()),
                role_name="Plumber",
                role_description="Professional plumber with 5+ years experience"
            ),
            models.Role(
                role_id=str(uuid.uuid4()),
                role_name="Carpenter",
                role_description="Skilled carpenter for woodwork and construction"
            ),
            models.Role(
                role_id=str(uuid.uuid4()),
                role_name="Painter",
                role_description="Interior and exterior painting specialist"
            ),
            models.Role(
                role_id=str(uuid.uuid4()),
                role_name="General Laborer",
                role_description="General construction and maintenance work"
            )
        ]
        for role in roles:
            db.add(role)
        db.flush()
        
        # Seed Workers
        print("Seeding workers...")
        workers = [
            models.Worker(
                worker_id=str(uuid.uuid4()),
                worker_first_name="Alice",
                worker_last_name="Johnson",
                worker_phone_number="+49 30 12345678",
                fk_branch_id=branches[0].branch_id
            ),
            models.Worker(
                worker_id=str(uuid.uuid4()),
                worker_first_name="Bob",
                worker_last_name="Smith",
                worker_phone_number="+49 30 23456789",
                fk_branch_id=branches[0].branch_id
            ),
            models.Worker(
                worker_id=str(uuid.uuid4()),
                worker_first_name="Charlie",
                worker_last_name="Brown",
                worker_phone_number="+49 30 34567890",
                fk_branch_id=branches[1].branch_id
            ),
            models.Worker(
                worker_id=str(uuid.uuid4()),
                worker_first_name="Diana",
                worker_last_name="Prince",
                worker_phone_number="+49 30 45678901",
                fk_branch_id=branches[1].branch_id
            ),
            models.Worker(
                worker_id=str(uuid.uuid4()),
                worker_first_name="Evan",
                worker_last_name="Wright",
                worker_phone_number="+49 30 56789012",
                fk_branch_id=branches[2].branch_id
            )
        ]
        for worker in workers:
            db.add(worker)
        db.flush()
        
        # Assign roles to workers
        print("Assigning roles to workers...")
        workers[0].roles.extend([roles[0], roles[4]])  # Alice: Electrician, General Laborer
        workers[1].roles.extend([roles[1], roles[4]])  # Bob: Plumber, General Laborer
        workers[2].roles.extend([roles[2]])            # Charlie: Carpenter
        workers[3].roles.extend([roles[3], roles[4]])  # Diana: Painter, General Laborer
        workers[4].roles.extend([roles[0], roles[1]])  # Evan: Electrician, Plumber
        
        # Seed Items
        print("Seeding items...")
        items = [
            models.Item(
                item_id=str(uuid.uuid4()),
                item_name="Power Drill",
                item_description="Professional cordless power drill with battery",
                fk_branch_id=branches[0].branch_id
            ),
            models.Item(
                item_id=str(uuid.uuid4()),
                item_name="Pipe Wrench",
                item_description="Heavy-duty adjustable pipe wrench",
                fk_branch_id=branches[0].branch_id
            ),
            models.Item(
                item_id=str(uuid.uuid4()),
                item_name="Hammer",
                item_description="Standard claw hammer",
                fk_branch_id=branches[1].branch_id
            ),
            models.Item(
                item_id=str(uuid.uuid4()),
                item_name="Paint Roller Set",
                item_description="Complete paint roller set with extensions",
                fk_branch_id=branches[1].branch_id
            ),
            models.Item(
                item_id=str(uuid.uuid4()),
                item_name="Safety Helmet",
                item_description="OSHA-approved safety helmet",
                fk_branch_id=branches[2].branch_id
            ),
            models.Item(
                item_id=str(uuid.uuid4()),
                item_name="Measuring Tape",
                item_description="25ft professional measuring tape",
                fk_branch_id=branches[2].branch_id
            )
        ]
        for item in items:
            db.add(item)
        db.flush()
        
        # Seed Stock
        print("Seeding stock...")
        stocks = [
            models.Stock(stock_id=str(uuid.uuid4()), quantity=10, fk_branch_id=branches[0].branch_id, fk_item_id=items[0].item_id),
            models.Stock(stock_id=str(uuid.uuid4()), quantity=8, fk_branch_id=branches[0].branch_id, fk_item_id=items[1].item_id),
            models.Stock(stock_id=str(uuid.uuid4()), quantity=15, fk_branch_id=branches[1].branch_id, fk_item_id=items[2].item_id),
            models.Stock(stock_id=str(uuid.uuid4()), quantity=12, fk_branch_id=branches[1].branch_id, fk_item_id=items[3].item_id),
            models.Stock(stock_id=str(uuid.uuid4()), quantity=20, fk_branch_id=branches[2].branch_id, fk_item_id=items[4].item_id),
            models.Stock(stock_id=str(uuid.uuid4()), quantity=18, fk_branch_id=branches[2].branch_id, fk_item_id=items[5].item_id),
            # Cross-branch stock
            models.Stock(stock_id=str(uuid.uuid4()), quantity=5, fk_branch_id=branches[1].branch_id, fk_item_id=items[0].item_id),
            models.Stock(stock_id=str(uuid.uuid4()), quantity=7, fk_branch_id=branches[2].branch_id, fk_item_id=items[2].item_id),
        ]
        for stock in stocks:
            db.add(stock)
        db.flush()
        
        # Seed Jobs
        print("Seeding jobs...")
        now = datetime.now()
        jobs = [
            models.Job(
                job_id=str(uuid.uuid4()),
                job_name="Office Electrical Installation",
                job_description="Install new electrical outlets and lighting in office building",
                longitude=13.388860,
                latitude=52.517037,
                country="Germany",
                city="Berlin",
                street="Friedrichstraße",
                house_number="123",
                postal_code="10117",
                start_datetime=now + timedelta(days=1, hours=8),
                end_datetime=now + timedelta(days=1, hours=12)
            ),
            models.Job(
                job_id=str(uuid.uuid4()),
                job_name="Residential Plumbing Repair",
                job_description="Fix bathroom plumbing issues in residential building",
                longitude=13.074410,
                latitude=52.395715,
                country="Germany",
                city="Potsdam",
                street="Friedrich-Ebert-Straße",
                house_number="56",
                postal_code="14469",
                start_datetime=now + timedelta(days=2, hours=9),
                end_datetime=now + timedelta(days=2, hours=13)
            ),
            models.Job(
                job_id=str(uuid.uuid4()),
                job_name="Furniture Assembly",
                job_description="Assemble and install custom furniture in new office",
                longitude=13.401270,
                latitude=52.520007,
                country="Germany",
                city="Berlin",
                street="Karl-Liebknecht-Straße",
                house_number="8",
                postal_code="10178",
                start_datetime=now + timedelta(days=3, hours=8),
                end_datetime=now + timedelta(days=3, hours=16)
            ),
            models.Job(
                job_id=str(uuid.uuid4()),
                job_name="Interior Painting",
                job_description="Paint walls and ceilings in renovated apartment",
                longitude=12.551742,
                latitude=52.408779,
                country="Germany",
                city="Brandenburg an der Havel",
                street="Steinstraße",
                house_number="34",
                postal_code="14776",
                start_datetime=now + timedelta(days=4, hours=7),
                end_datetime=now + timedelta(days=4, hours=15)
            )
        ]
        for job in jobs:
            db.add(job)
        db.flush()
        
        # Assign roles to jobs
        print("Assigning roles and items to jobs...")
        jobs[0].roles.append(roles[0])  # Electrician
        jobs[1].roles.append(roles[1])  # Plumber
        jobs[2].roles.extend([roles[2], roles[4]])  # Carpenter, General Laborer
        jobs[3].roles.extend([roles[3], roles[4]])  # Painter, General Laborer
        
        # Assign items to jobs via JobItem
        job_items = [
            models.JobItem(job_id=jobs[0].job_id, item_id=items[0].item_id, required_quantity=2),  # Power Drill
            models.JobItem(job_id=jobs[0].job_id, item_id=items[4].item_id, required_quantity=1),  # Safety Helmet
            models.JobItem(job_id=jobs[1].job_id, item_id=items[1].item_id, required_quantity=1),  # Pipe Wrench
            models.JobItem(job_id=jobs[1].job_id, item_id=items[4].item_id, required_quantity=1),  # Safety Helmet
            models.JobItem(job_id=jobs[2].job_id, item_id=items[2].item_id, required_quantity=3),  # Hammer
            models.JobItem(job_id=jobs[2].job_id, item_id=items[5].item_id, required_quantity=2),  # Measuring Tape
            models.JobItem(job_id=jobs[3].job_id, item_id=items[3].item_id, required_quantity=2),  # Paint Roller Set
            models.JobItem(job_id=jobs[3].job_id, item_id=items[4].item_id, required_quantity=1),  # Safety Helmet
        ]
        for job_item in job_items:
            db.add(job_item)
        
        db.commit()
        print(f"Successfully seeded database:")
        print(f"  - {len(branches)} branches")
        print(f"  - {len(roles)} roles")
        print(f"  - {len(workers)} workers")
        print(f"  - {len(items)} items")
        print(f"  - {len(stocks)} stocks")
        print(f"  - {len(jobs)} jobs")
        
        # Run planner
        print("\nRunning planner to assign workers...")
        fetch_and_run_planner(db, debug=True)
        print("Planner completed.")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
