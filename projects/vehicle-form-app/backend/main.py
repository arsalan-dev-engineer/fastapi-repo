from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
from typing import List, Optional

# -----------------------------
# FastAPI App Setup
# -----------------------------
app = FastAPI()

# Allowed frontend origins for CORS
origins = [
    "http://localhost:5173",  # React dev server
    "http://127.0.0.1:5173",
]

# Add CORS middleware so React can make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # allowed origins
    allow_credentials=True,     # allow cookies
    allow_methods=["*"],        # allow all HTTP methods
    allow_headers=["*"],        # allow all headers
)

# -----------------------------
# Pydantic Model
# -----------------------------


class Vehicle(BaseModel):
    # Unique ID, automatically assigned when creating a vehicle
    id: Optional[str] = None
    # Vehicle details
    make: str
    model: str
    year: int
    colour: str
    body: str
    doors: int
    transmission: str
    engineSize: float
    fuel: str


# -----------------------------
# In-Memory "Database"
# -----------------------------
# Stores all Vehicle objects
vehicles: List[Vehicle] = []

# -----------------------------
# Endpoints
# -----------------------------


@app.get("/")
async def landing_page():
    """
    Landing page for API
    """
    return {"message": "Welcome to the vehicle database."}


# =============================

@app.get("/vehicle/")
async def get_all_vehicles():
    """
    Return all vehicles currently in memory
    """
    return vehicles


# =============================

@app.get("/vehicle/{vehicle_id}")
async def get_vehicle(vehicle_id: str):
    """
    Return a single vehicle by its unique ID.
    Uses dot notation because vehicles are Pydantic objects.
    Raises 404 if vehicle not found.
    """
    for vehicle in vehicles:
        if vehicle.id == vehicle_id:
            return vehicle
    raise HTTPException(status_code=404, detail="Vehicle not found")


# =============================

@app.post("/vehicle/")
def create_vehicle(vehicle: Vehicle):
    """
    Create a new vehicle.
    Automatically assigns a unique UUID as the vehicle ID.
    Appends the vehicle to the in-memory list.
    """
    # Assign a new UUID
    vehicle.id = str(uuid4())

    # Add vehicle to "database"
    vehicles.append(vehicle)

    # Return confirmation + vehicle data
    return {"message": "Vehicle received!", "data": vehicle}


# =============================

@app.put("/vehicle/{vehicle_id}")
def update_vehicle(vehicle_id: str, updated_vehicle: Vehicle):
    for idx, vehicle in enumerate(vehicles):
        if vehicle.id == vehicle_id:
            updated_vehicle.id = vehicle_id  # keep the same ID
            vehicles[idx] = updated_vehicle
            return {"message": "Vehicle updated", "data": updated_vehicle}
    raise HTTPException(status_code=404, detail="Vehicle not found")


# =============================

@app.delete("/vehicle/{vehicle_id}")
def delete_vehicle(vehicle_id: str):
    for idx, vehicle in enumerate(vehicles):
        if vehicle.id == vehicle_id:
            removed = vehicles.pop(idx)
            return {"message": "Vehicle deleted", "data": removed}
    raise HTTPException(status_code=404, detail="Vehicle not found")
