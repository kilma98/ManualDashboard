from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.db import get_db
from core.deps import get_current_user
from core.telegram import send_telegram_message
from models.measurement import Measurement
from models.threshold import Threshold
from models.user import User
from schemas.measurement import MeasurementCreate, MeasurementOut, MeasurementCreateResponse


router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.post("/", response_model=MeasurementCreateResponse)
def add_measurement(payload: MeasurementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    timestamp = payload.timestamp or datetime.utcnow()
    measurement = Measurement(
        user_id=current_user.id,
        ph=payload.ph,
        ec=payload.ec,
        oxygen=payload.oxygen,
        humidity=payload.humidity,
        temperature=payload.temperature,
        water_temperature=payload.water_temperature,
        timestamp=timestamp
    )
    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    # Check thresholds (user-specific first, fallback to global)
    threshold = (
        db.query(Threshold)
        .filter((Threshold.user_id == current_user.id) | (Threshold.user_id.is_(None)))
        .order_by(Threshold.user_id.desc())
        .first()
    )
    alerts: list[str] = []
    if threshold:
        if not (threshold.ph_min <= measurement.ph <= threshold.ph_max):
            alerts.append(f"pH {measurement.ph} out of [{threshold.ph_min}, {threshold.ph_max}]")
        if not (threshold.ec_min <= measurement.ec <= threshold.ec_max):
            alerts.append(f"EC {measurement.ec} out of [{threshold.ec_min}, {threshold.ec_max}]")
        if not (threshold.oxygen_min <= measurement.oxygen <= threshold.oxygen_max):
            alerts.append(
                f"Oxygen {measurement.oxygen} out of [{threshold.oxygen_min}, {threshold.oxygen_max}]"
            )
    if alerts:
        send_telegram_message(
            f"Alert for user {current_user.username}: " + "; ".join(alerts)
        )

    return {"measurement": measurement, "alerts": alerts}


@router.get("/", response_model=list[MeasurementOut])
def list_my_measurements(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(Measurement)
        .filter(Measurement.user_id == current_user.id)
        .order_by(Measurement.timestamp.desc())
        .all()
    )