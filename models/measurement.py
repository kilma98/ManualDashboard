from datetime import datetime

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from core.db import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    ph = Column(Float, nullable=False)
    ec = Column(Float, nullable=False)
    oxygen = Column(Float, nullable=False)
    temperature = Column(Float,nullable=False)
    water_temperature = Column(Float,nullable=False)
    humidity = Column(Float,nullable=False)  # %
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="measurements")


