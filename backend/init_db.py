import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.core.database import Base, engine
from app.models import models
from seed.seed import seed_database

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
    
    print("\nSeeding database with initial data...")
    seed_database()
    print("Database seeding completed!")

if __name__ == "__main__":
    init_db()
