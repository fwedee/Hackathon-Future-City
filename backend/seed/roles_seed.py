import uuid
from app.models import models


def seed_roles():
    """Seed roles data"""
    roles = [
        models.Role(
            role_id=str(uuid.uuid4()),
            role_name="Electrician",
            role_description="Licensed electrician with certification for electrical installations"
        ),
        models.Role(
            role_id=str(uuid.uuid4()),
            role_name="Plumber",
            role_description="Professional plumber with expertise in water and drainage systems"
        ),
        models.Role(
            role_id=str(uuid.uuid4()),
            role_name="Carpenter",
            role_description="Skilled carpenter for woodwork, furniture assembly, and construction"
        ),
        models.Role(
            role_id=str(uuid.uuid4()),
            role_name="Painter",
            role_description="Interior and exterior painting specialist with color expertise"
        ),
        models.Role(
            role_id=str(uuid.uuid4()),
            role_name="HVAC Technician",
            role_description="Heating, ventilation, and air conditioning systems specialist"
        ),
        models.Role(
            role_id=str(uuid.uuid4()),
            role_name="General Laborer",
            role_description="General construction and maintenance work, assists all trades"
        )
    ]
    
    return roles
