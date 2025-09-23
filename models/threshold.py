from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class Threshold(Base):
    __tablename__ = "thresholds"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    ph_min = Column(Float, nullable=False)
    ph_max = Column(Float, nullable=False)
    ec_min = Column(Float, nullable=False)
    ec_max = Column(Float, nullable=False)
    oxygen_min = Column(Float, nullable=False)
    oxygen_max = Column(Float, nullable=False)

    user = relationship("User", back_populates="thresholds")


