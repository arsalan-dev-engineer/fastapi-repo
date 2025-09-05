from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# To load environment variables from a .env file
from dotenv import load_dotenv
import os

# load env variables from .env file into project
load_dotenv()

# read PostgreSQL credentials from .env
DB_USER = os.getenv("V_DB_USER")
DB_PASSWORD = os.getenv("V_DB_PASSWORD")
DB_HOST = os.getenv("V_DB_HOST")
DB_PORT = os.getenv("V_DB_PORT")
DB_NAME = os.getenv("V_DB_NAME")

# build the full database URL for SQLAlchemy
# format:
# postgresql://user:password@host:port/dbname
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# create SQLAlchemy engine (connects to the database)
engine = create_engine(DATABASE_URL)

# create a configured "Session class"
# autocommit=False -> changes are not saved automatically
# autoflush=False -> changes are not flushed until commit()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for SQLAlchemy models (used to define tables)
Base = declarative_base()


# dependency to get a database session for FastAPI routes
def get_db():
    # create a new session
    db = SessionLocal()
    try:
        # provide the session to the route
        yield db
    finally:
        # close the session after the request is done
        db.close()
