from __future__ import annotations
from pydantic import BaseModel


class ThresholdUpsert(BaseModel):
    user_id: int | None = None
    ph_min: float
    ph_max: float
    ec_min: float
    ec_max: float
    oxygen_min: float
    oxygen_max: float


class ThresholdOut(BaseModel):
    id: int
    user_id: int | None
    ph_min: float
    ph_max: float
    ec_min: float
    ec_max: float
    oxygen_min: float
    oxygen_max: float

    class Config:
        from_attributes = True


