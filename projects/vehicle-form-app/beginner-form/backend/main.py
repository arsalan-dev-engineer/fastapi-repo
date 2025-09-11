# ================================
# main.py - FastAPI app with Users + Vehicles
# ================================

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# Import database models and DB session dependency
from database import get_db, User, Vehicle

# -----------------------------
# FastAPI App Setup
# -----------------------------
app = FastAPI()

# CORS settings: Allows your React frontend to make requests
# Without this, the browser will block cross-origin requests
origins = [
    "http://localhost:5173",  # React dev server default
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Which frontend URLs are allowed
    allow_credentials=True,     # Allow cookies if needed
    allow_methods=["*"],        # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # Allow all headers
)

# -----------------------------
# Pydantic Schemas
# -----------------------------
# Pydantic models define the "shape" of data sent to/returned from API
# They validate inputs and control JSON serialization

# User schemas


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    name: str
    email: str


class UserOut(UserCreate):
    """Schema for returning user info (includes ID)"""
    id: int

    class Config:
        # allows SQLAlchemy objects to be converted to JSON automatically
        from_attributes = True

# Vehicle schemas


class VehicleCreate(BaseModel):
    """Schema for creating a vehicle"""
    make: str
    model: str
    year: int
    colour: str
    body: str
    doors: int
    transmission: str
    engineSize: float
    fuel: str


class VehicleOut(VehicleCreate):
    """Schema for returning a vehicle (includes ID)"""
    id: int

    class Config:
        from_attributes = True

# -----------------------------
# Root endpoint
# -----------------------------


@app.get("/")
def landing_page():
    """Simple landing page to confirm API is running"""
    return {"message": "Welcome to the vehicle + user database."}

# =============================
# User Endpoints (DB-backed)
# =============================


@app.get("/users", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    """
    GET all users from the database.
    - db: SQLAlchemy session injected via Depends()
    - returns a list of users
    """
    return db.query(User).all()  # simple SELECT * FROM users


@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    POST a new user to the database.
    - user: validated Pydantic model
    - db: SQLAlchemy session
    """
    new_user = User(name=user.name, email=user.email)  # create ORM object
    db.add(new_user)        # stage the object to be added
    db.commit()             # save it to the DB
    db.refresh(new_user)    # refresh to get auto-generated ID
    return new_user         # returned as JSON using UserOut schema

# =============================
# Vehicle Endpoints (DB-backed)
# =============================


@app.get("/vehicles", response_model=List[VehicleOut])
def get_all_vehicles(db: Session = Depends(get_db)):
    """
    GET all vehicles from the database
    """
    return db.query(Vehicle).all()  # SELECT * FROM vehicles


@app.get("/vehicles/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """
    GET a single vehicle by its ID
    - Raises 404 if vehicle not found
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@app.post("/vehicles", response_model=VehicleOut)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """
    POST a new vehicle to the database
    - vehicle: validated Pydantic model
    """
    new_vehicle = Vehicle(**vehicle.model_dump())  # unpack dict into ORM model
    db.add(new_vehicle)      # stage object
    db.commit()              # save to DB
    db.refresh(new_vehicle)  # get generated ID
    return new_vehicle


@app.put("/vehicles/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(
    vehicle_id: int,
    updated_vehicle: VehicleCreate,
    db: Session = Depends(get_db)
):
    """
    PUT: Update a vehicle's data
    - Find vehicle by ID
    - Update fields using setattr
    - Save changes
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Loop through fields in request and update ORM object
    for key, value in updated_vehicle.model_dump().items():
        setattr(vehicle, key, value)

    db.commit()              # save updates
    db.refresh(vehicle)      # refresh ORM object
    return vehicle


@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """
    DELETE a vehicle by ID
    - Raises 404 if not found
    - Commits deletion to DB
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(vehicle)  # stage deletion
    db.commit()         # execute deletion
    return {"message": "Vehicle deleted", "id": vehicle_id}
