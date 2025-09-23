from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field


class MeasurementCreate(BaseModel):
    ph: float = Field(..., ge=0, le=14)
    ec: float
    oxygen: float
    timestamp: datetime | None = None
    humidity: float | None
    temperature: float | None
    water_temperature: float | None


class MeasurementOut(BaseModel):
    id: int
    user_id: int
    ph: float
    ec: float
    oxygen: float
    timestamp: datetime
    humidity: float 
    temperature: float 
    water_temperature: float 

    class Config:
        from_attributes = True
        orm_mode = True


class MeasurementCreateResponse(BaseModel):
    measurement: MeasurementOut
    alerts: list[str] = []
    


