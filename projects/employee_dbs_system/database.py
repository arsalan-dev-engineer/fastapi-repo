from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# To load environment variables from a .env file
from dotenv import load_dotenv
import os

# Load environment variables from a .env file in your project
load_dotenv()

# Read PostgreSQL credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Build the full database URL for SQLAlchemy
# Format: postgresql://user:password@host:port/dbname
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create the SQLAlchemy engine (connects to the database)
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
# autocommit=False -> changes are not saved automatically
# autoflush=False -> changes are not flushed until commit()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models (used to define tables)
Base = declarative_base()


# Dependency to get a database session for FastAPI routes
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Provide the session to the route
    finally:
        db.close()  # Close the session after the request is done
