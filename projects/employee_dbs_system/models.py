from sqlalchemy import Column, Integer, String
from database import Base  # Base class for SQLAlchemy models


# Define the Employee table
class Employee(Base):
    __tablename__ = "employees"  # Name of the table in PostgreSQL

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    # 'id' is the primary key (unique identifier), indexed for faster lookups

    name = Column(String, index=True)
    # 'name' column stores employee name, indexed for faster search

    position = Column(String)
    # 'position' column stores employee job title/position
