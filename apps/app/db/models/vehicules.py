import uuid
from sqlalchemy import Column, String, Integer, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_number = Column(String, unique=True, nullable=False)
    vin = Column(String, nullable=True, index=True)

    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    mileage = Column(Integer, nullable=True)
    in_service_date = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
