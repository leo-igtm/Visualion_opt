import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base



DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/visualion_db")
Base = declarative_base()


create_engine(DATABASE_URL, echo=True)

class DatabaseConnection:
    _instance = None

    def __init__(self):
        if DatabaseConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseConnection._instance = self
            self.connection = self.create_connection()

    @staticmethod
    def get_instance():
        if DatabaseConnection._instance is None:
            DatabaseConnection()
        return DatabaseConnection._instance

    def create_connection(self):
        # Aquí puedes implementar la lógica para crear la conexión a la base de datos
        # Por ejemplo, usando SQLAlchemy o cualquier otro ORM
        # return create_engine(DATABASE_URL)
        pass


if __name__ == "__main__":
    # Test the database connection
    try:
        db = DatabaseConnection.get_instance()
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")