import uuid
from app.models import models


def seed_workers(branches, roles):
    """Seed workers data with role assignments"""
    workers_data = [
        # Berlin Branch Workers
        ("Alice", "Johnson", "+49 30 12345678", 0, [0, 5]),  # Electrician, General Laborer
        ("Bob", "Smith", "+49 30 23456789", 0, [1, 5]),      # Plumber, General Laborer
        ("Charlie", "Brown", "+49 30 34567890", 0, [2]),     # Carpenter
        ("Diana", "Prince", "+49 30 45678901", 0, [3, 5]),   # Painter, General Laborer
        ("Evan", "Wright", "+49 30 56789012", 0, [0, 1]),    # Electrician, Plumber
        ("Fiona", "Green", "+49 30 67890123", 0, [4]),       # HVAC Technician
        ("George", "Miller", "+49 30 78901234", 0, [2, 5]),  # Carpenter, General Laborer
        
        # Potsdam Branch Workers
        ("Hannah", "Davis", "+49 331 12345678", 1, [0]),     # Electrician
        ("Ivan", "Garcia", "+49 331 23456789", 1, [1, 4]),   # Plumber, HVAC Technician
        ("Julia", "Martinez", "+49 331 34567890", 1, [3]),   # Painter
        ("Kevin", "Rodriguez", "+49 331 45678901", 1, [2, 5]), # Carpenter, General Laborer
        ("Laura", "Wilson", "+49 331 56789012", 1, [0, 5]),  # Electrician, General Laborer
        ("Michael", "Anderson", "+49 331 67890123", 1, [4]), # HVAC Technician
        ("Nina", "Taylor", "+49 331 78901234", 1, [1, 5]),   # Plumber, General Laborer
        
        # Brandenburg Branch Workers
        ("Oliver", "Thomas", "+49 3381 12345678", 2, [2]),   # Carpenter
        ("Paula", "Moore", "+49 3381 23456789", 2, [3, 5]),  # Painter, General Laborer
        ("Quinn", "Jackson", "+49 3381 34567890", 2, [0, 4]), # Electrician, HVAC Technician
        ("Rachel", "White", "+49 3381 45678901", 2, [1]),    # Plumber
        ("Samuel", "Harris", "+49 3381 56789012", 2, [2, 5]), # Carpenter, General Laborer
        ("Tina", "Clark", "+49 3381 67890123", 2, [3, 0]),   # Painter, Electrician
    ]
    
    workers = []
    for first_name, last_name, phone, branch_idx, role_indices in workers_data:
        worker = models.Worker(
            worker_id=str(uuid.uuid4()),
            worker_first_name=first_name,
            worker_last_name=last_name,
            worker_phone_number=phone,
            fk_branch_id=branches[branch_idx].branch_id
        )
        # Assign roles
        for role_idx in role_indices:
            worker.roles.append(roles[role_idx])
        workers.append(worker)
    
    return workers
