from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.db import get_db
from core.deps import require_admin
from models.measurement import Measurement
from models.threshold import Threshold
from models.user import User
from schemas.threshold import ThresholdOut, ThresholdUpsert
from schemas.user import UserOut
from schemas.measurement import MeasurementOut


router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/measurements", response_model=list[MeasurementOut])
def list_all_measurements(db: Session = Depends(get_db)):
    return db.query(Measurement).order_by(Measurement.timestamp.desc()).all()


@router.post("/thresholds", response_model=ThresholdOut)
def upsert_threshold(payload: ThresholdUpsert, db: Session = Depends(get_db)):
    # If user_id provided, upsert for that user; else global (user_id is NULL)
    q = db.query(Threshold)
    if payload.user_id is None:
        existing = q.filter(Threshold.user_id.is_(None)).first()
    else:
        existing = q.filter(Threshold.user_id == payload.user_id).first()

    if existing:
        for field in (
            "ph_min",
            "ph_max",
            "ec_min",
            "ec_max",
            "oxygen_min",
            "oxygen_max",
        ):
            setattr(existing, field, getattr(payload, field))
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    new_th = Threshold(
        user_id=payload.user_id,
        ph_min=payload.ph_min,
        ph_max=payload.ph_max,
        ec_min=payload.ec_min,
        ec_max=payload.ec_max,
        oxygen_min=payload.oxygen_min,
        oxygen_max=payload.oxygen_max,
    )
    db.add(new_th)
    db.commit()
    db.refresh(new_th)
    return new_th


@router.get("/thresholds", response_model=list[ThresholdOut])
def get_thresholds(db: Session = Depends(get_db)):
    return db.query(Threshold).all()

@router.get("/users/{user_id}/measurements", response_model=list[MeasurementOut])
def get_user_measurements(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    measurements = (
        db.query(Measurement)
        .filter(Measurement.user_id == user_id)
        .order_by(Measurement.timestamp.desc())
        .   all()
    )
    print("measurements fetched")
    print("Serialized measurements:", jsonable_encoder(measurements))

    return  db.query(Measurement) .filter(Measurement.user_id == user_id).order_by(Measurement.timestamp.desc()).all()


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()



@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




