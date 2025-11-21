import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.core.database import Base, engine
from app.models import models

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
