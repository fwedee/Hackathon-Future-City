import uuid
from app.models import models


def seed_items(branches):
    """Seed items data"""
    items = [
        models.Item(
            item_id=str(uuid.uuid4()),
            item_name="Power Drill",
            item_description="Professional cordless power drill with battery pack and charger",
            fk_branch_id=branches[0].branch_id
        ),
        models.Item(
            item_id=str(uuid.uuid4()),
            item_name="Pipe Wrench Set",
            item_description="Heavy-duty adjustable pipe wrench set (3 sizes)",
            fk_branch_id=branches[0].branch_id
        ),
        models.Item(
            item_id=str(uuid.uuid4()),
            item_name="Carpentry Tool Kit",
            item_description="Complete carpenter's toolkit with saw, hammer, chisels, and measuring tools",
            fk_branch_id=branches[1].branch_id
        ),
        models.Item(
            item_id=str(uuid.uuid4()),
            item_name="Paint Roller & Brush Set",
            item_description="Professional painting set with rollers, brushes, trays, and extensions",
            fk_branch_id=branches[1].branch_id
        ),
        models.Item(
            item_id=str(uuid.uuid4()),
            item_name="HVAC Diagnostic Tools",
            item_description="HVAC system diagnostic and repair toolset with gauges",
            fk_branch_id=branches[2].branch_id
        ),
        models.Item(
            item_id=str(uuid.uuid4()),
            item_name="Safety Equipment Pack",
            item_description="Complete safety gear: helmet, goggles, gloves, high-vis vest, safety boots",
            fk_branch_id=branches[2].branch_id
        )
    ]
    
    return items
