from sqlalchemy import Column, Integer, String, Boolean, Float
from .database import Base

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, unique=True, index=True)
    technician_name = Column(String)
    is_hazardous = Column(Boolean, default=False)
    temperature_celsius = Column(Float, nullable=True)