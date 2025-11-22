import uuid
import sys
import os

# Add current directory to sys.path to allow importing app modules
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models import models

def seed_workers():
    db = SessionLocal()
    
    workers_data = [
        {"name": "Alice Johnson", "worker_id": str(uuid.uuid4())},
        {"name": "Bob Smith", "worker_id": str(uuid.uuid4())},
        {"name": "Charlie Brown", "worker_id": str(uuid.uuid4())},
        {"name": "Diana Prince", "worker_id": str(uuid.uuid4())},
        {"name": "Evan Wright", "worker_id": str(uuid.uuid4())},
    ]

    print("Seeding workers...")
    for w_data in workers_data:
        # Check if worker exists (optional, but good for re-running)
        # For simplicity, we just add them.
        worker = models.Worker(worker_id=w_data["worker_id"], name=w_data["name"])
        db.add(worker)
    
    try:
        db.commit()
        print(f"Successfully added {len(workers_data)} workers.")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_workers()
