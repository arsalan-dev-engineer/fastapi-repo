from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db  # Import DB connection & session
from models import Employee  # Import Employee model

# Initialize FastAPI app
app = FastAPI()

# Create database tables based on SQLAlchemy models (runs at startup)
Base.metadata.create_all(bind=engine)


# Root endpoint to test if FastAPI + PostgreSQL is working
@app.get("/")
def root():
    return {"message": "FastAPI + PostgreSQL is working!"}


# POST endpoint to create a new employee
@app.post("/employees/")
def create_employee(
    name: str,  # Employee name from query/form parameters
    position: str,  # Employee position from query/form parameters
    db: Session = Depends(get_db)  # Database session injected by FastAPI
):
    # Create a new Employee object
    employee = Employee(name=name, position=position)
    db.add(employee)  # Add to session
    db.commit()  # Commit to database
    # Refresh object to get DB-generated fields (e.g., id)
    db.refresh(employee)
    return employee  # Return the newly created employee


# GET endpoint to read all employees from the database
@app.get("/employees/")
def read_employees(db: Session = Depends(get_db)):
    # Query all Employee records
    return db.query(Employee).all()
