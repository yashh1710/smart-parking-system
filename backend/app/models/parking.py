from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)

    manufacturer = Column(String(100), nullable=False, index=True)
    model = Column(String(100), nullable=False, index=True)
    variant = Column(String(100), nullable=True)

    model_year = Column(Integer, nullable=True)

    vehicle_type = Column(String(50), nullable=False)

    length_mm = Column(Float, nullable=False)
    width_mm = Column(Float, nullable=False)
    height_mm = Column(Float, nullable=False)
    wheelbase_mm = Column(Float, nullable=True)

    source_name = Column(String(150), nullable=True)
    source_url = Column(String(500), nullable=True)
    dimension_notes = Column(String(500), nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )


class ParkingLot(Base):
    __tablename__ = "parking_lots"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    length_mm = Column(Float, nullable=False)
    width_mm = Column(Float, nullable=False)

    road_width_mm = Column(Float, nullable=False)
    parking_angle = Column(Float, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)

    lot_id = Column(
        Integer,
        ForeignKey("parking_lots.id"),
        nullable=False
    )

    slot_number = Column(String(20), nullable=False)

    length_mm = Column(Float, nullable=False)
    width_mm = Column(Float, nullable=False)
    height_mm = Column(Float, nullable=False)

    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

    angle = Column(Float, nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="AVAILABLE"
    )