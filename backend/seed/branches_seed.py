import uuid
from app.models import models


def seed_branches():
    """Seed branches data"""
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
    
    return branches
