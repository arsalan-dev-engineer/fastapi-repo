from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime, timezone
from models import BodyTypeEnum, TransmissionEnum, FuelTypeEnum


class VehicleCreate(BaseModel):
    """
    Pydantic model for creating a new vehicle (user input).

    Only includes fields the user can provide:
    - make, model, body_type, engine_size, transmission
    - vehicle_age, fuel_type, colour, vehicle_price

    Validation:
    - engine_size must be > 0
    - vehicle_age must be >= 0
    - vehicle_price must be >= 0
    """
    make: str
    model: str
    body_type: BodyTypeEnum
    engine_size: float = Field(gt=0)
    transmission: TransmissionEnum
    vehicle_age: int = Field(ge=0)
    fuel_type: FuelTypeEnum
    colour: str
    vehicle_price: float = Field(ge=0)


class VehicleOut(BaseModel):
    """
    Pydantic model for returning vehicle data to the frontend.

    Includes all fields, including system-managed:
    - id (UUID)
    - created_at / updated_at timestamps
    - is_available (soft delete flag)

    Automatically converts SQLAlchemy objects to Pydantic models.
    Ensures timestamps are timezone-aware.
    """
    id: UUID
    make: str
    model: str
    body_type: BodyTypeEnum
    engine_size: float
    transmission: TransmissionEnum
    vehicle_age: int
    fuel_type: FuelTypeEnum
    colour: str
    vehicle_price: float
    created_at: datetime
    updated_at: datetime
    is_available: bool

    model_config = {
        "from_attributes": True
    }

    @field_validator("created_at", "updated_at")
    def must_have_timezone(cls, v: datetime) -> datetime:
        """
        Ensures that datetime fields include timezone info (UTC).
        If naive, sets timezone to UTC automatically.
        """
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
