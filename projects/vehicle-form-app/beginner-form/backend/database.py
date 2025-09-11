from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# ------------------------------
# 1. Database setup
# ------------------------------
# Change this line when you want to use MySQL instead of SQLite.
# Example for MySQL:
# SQLALCHEMY_DATABASE_URL = ""
SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://myuser:Password24!@localhost:3306/vehicle_form_dbs"
)

# Create the SQLAlchemy engine (manages the DB connection pool)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False}
    if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Session factory: every request will get its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class: all DB models must inherit from this
Base = declarative_base()

# ------------------------------
# 2. Define Models (Tables)
# ------------------------------


# Users table
class User(Base):
    __tablename__ = "users"  # SQL table name
    # auto-increment primary key
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)   # max 255 chars
    email = Column(String(255), unique=True, index=True)


# Vehicles table
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(255), index=True)
    model = Column(String(255), index=True)
    year = Column(Integer, index=True)
    colour = Column(String(100))
    body = Column(String(100))
    doors = Column(Integer, index=True)
    transmission = Column(String(50))
    engineSize = Column(Float, index=True)
    fuel = Column(String(50))


# ------------------------------
# 3. Create tables (once)
# ------------------------------
# If tables don’t exist yet, this will create them
Base.metadata.create_all(bind=engine)


# ------------------------------
# 4. Dependency: DB session
# ------------------------------
def get_db():
    """Yields a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
