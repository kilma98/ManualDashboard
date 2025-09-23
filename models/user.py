
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(10), nullable=False, default="user")

    measurements = relationship("Measurement", back_populates="user", cascade="all, delete-orphan")
    thresholds = relationship("Threshold", back_populates="user", cascade="all, delete-orphan")


