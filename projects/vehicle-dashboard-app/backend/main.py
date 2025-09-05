from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import Base, engine, get_db
from models import Vehicle
from schemas import VehicleCreate, VehicleOut

app = FastAPI()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


# =====================
# ROOT
# =====================
@app.get("/")
async def root():
    return {"message": "Welcome to Vehicle Database System"}


# =====================
# GET ALL VEHICLES
# =====================
@app.get("/vehicles/", response_model=list[VehicleOut])
def read_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    return vehicles  # FastAPI + VehicleOut will serialize properly


# =====================
# POST endpoint
# =====================
@app.post("/vehicles/", response_model=VehicleOut, status_code=201)
def create_vehicle(vehicle_data: VehicleCreate, db: Session = Depends(get_db)):
    try:
        # Map Pydantic input to SQLAlchemy model
        vehicle = Vehicle(**vehicle_data.model_dump())
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return vehicle

    except SQLAlchemyError as e:
        db.rollback()  # undo changes if error occurs
        raise HTTPException(
            status_code=400,
            detail=f"Could not create vehicle: {str(e)}"
        )
