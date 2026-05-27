import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/visualion_db")
engine = create_engine(DATABASE_URL)

class DatabaseConnection:
    isinstance  = None

    @classmethod
    def get_instance(cls):
        if cls.isinstance is None:
            cls.isinstance = sessionmaker(bind=engine)()
        return cls.isinstance
    
Base = declarative_base()

if __name__ == "__main__":
    # Test the database connection
    try:
        db = DatabaseConnection.get_instance()
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")

