from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from datetime import datetime, timezone
from database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum


# =====================
# Enums = fixed choices
# =====================
class TransmissionEnum(PyEnum):
    manual = "Manual"
    automatic = "Automatic"


class FuelTypeEnum(PyEnum):
    petrol = "Petrol"
    diesel = "Diesel"
    hybrid = "Hybrid"
    electric = "Electric"
    plugin_hybrid = "Plugin Hybrid"


class BodyTypeEnum(PyEnum):
    cabriolet = "Cabriolet"
    coupe = "Coupe"
    estate = "Estate"
    hatchback = "Hatchback"
    mpv = "MPV"
    saloon = "Saloon"
    van = "Van"
    suv = "SUV"


class Vehicle(Base):
    __tablename__ = "vehicles"

    # system-generated
    id = Column(PG_UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_available = Column(Boolean, default=True)

    # user-provided
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    body_type = Column(
        SQLEnum(BodyTypeEnum, name="body_type_enum"), nullable=False)

    engine_size = Column(Float, nullable=False)
    transmission = Column(
        SQLEnum(TransmissionEnum, name="transmission_enum"), nullable=False)

    vehicle_age = Column(Integer, nullable=False)
    fuel_type = Column(
        SQLEnum(FuelTypeEnum, name="fuel_type_enum"), nullable=False)

    colour = Column(String, nullable=False)
    vehicle_price = Column(Float, nullable=False)
