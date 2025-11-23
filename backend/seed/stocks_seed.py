import uuid
from app.models import models


def seed_stocks(branches, items):
    """Seed stock data - requires branches and items"""
    stocks = [
        # Berlin warehouse stock
        models.Stock(stock_id=str(uuid.uuid4()), quantity=15, fk_branch_id=branches[0].branch_id, fk_item_id=items[0].item_id),
        models.Stock(stock_id=str(uuid.uuid4()), quantity=12, fk_branch_id=branches[0].branch_id, fk_item_id=items[1].item_id),
        models.Stock(stock_id=str(uuid.uuid4()), quantity=8, fk_branch_id=branches[0].branch_id, fk_item_id=items[5].item_id),
        
        # Potsdam warehouse stock
        models.Stock(stock_id=str(uuid.uuid4()), quantity=10, fk_branch_id=branches[1].branch_id, fk_item_id=items[2].item_id),
        models.Stock(stock_id=str(uuid.uuid4()), quantity=20, fk_branch_id=branches[1].branch_id, fk_item_id=items[3].item_id),
        models.Stock(stock_id=str(uuid.uuid4()), quantity=6, fk_branch_id=branches[1].branch_id, fk_item_id=items[0].item_id),
        models.Stock(stock_id=str(uuid.uuid4()), quantity=12, fk_branch_id=branches[1].branch_id, fk_item_id=items[5].item_id),
        
        # Brandenburg warehouse stock
        models.Stock(stock_id=str(uuid.uuid4()), quantity=8, fk_branch_id=branches[2].branch_id, fk_item_id=items[4].item_id),
        models.Stock(stock_id=str(uuid.uuid4()), quantity=15, fk_branch_id=branches[2].branch_id, fk_item_id=items[5].item_id),
        models.Stock(stock_id=str(uuid.uuid4()), quantity=5, fk_branch_id=branches[2].branch_id, fk_item_id=items[2].item_id),
        models.Stock(stock_id=str(uuid.uuid4()), quantity=7, fk_branch_id=branches[2].branch_id, fk_item_id=items[3].item_id),
    ]
    
    return stocks
