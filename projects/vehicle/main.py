from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# initial FastAPI application
app = FastAPI(title="Vehicle API System.")


# pydantic model (schema for request/response)
class Vehicle(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    transmission: str
    color: Optional[str] = None  # color (optional)


# in-memory database
# list will reset on restart
vehicles: List[Vehicle] = []


@app.get("/vehicles", response_model=List[Vehicle])
async def read_root():
    # return all vehicles in-memory
    return vehicles


# CRUD endpoints
@app.post("/vehicles/", response_model=Vehicle)
def create_vehicle(vehicle: Vehicle):
    # add new vehicle to the database (list)
    vehicles.append(vehicle)
    return vehicle


@app.get("/vehicles/{vehicle_id}", response_model=Vehicle)
def get_vehicle(vehicle_id: int):
    # loop through vehicles to find match
    for v in vehicles:
        if v.id == vehicle_id:
            return v
    # if not found, raise 404
    raise HTTPException(status_code=404, detail="Vehicle not found.")


# UPDATE: Update a vehicle by ID
@app.put("/vehicles/{vehicle_id}", response_model=Vehicle)
def update_vehicle(vehicle_id: int, updated_vehicle: Vehicle):
    for idx, v in enumerate(vehicles):
        if v.id == vehicle_id:
            # Replace old vehicle with new one
            vehicles[idx] = updated_vehicle
            return updated_vehicle
    raise HTTPException(status_code=404, detail="Vehicle not found")


# DELETE: Remove a vehicle by ID
@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int):
    for idx, v in enumerate(vehicles):
        if v.id == vehicle_id:
            vehicles.pop(idx)  # Remove vehicle from list
            return {"message": "Vehicle deleted successfully"}
    raise HTTPException(status_code=404, detail="Vehicle not found")
