from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    movements = relationship("Movement", back_populates="owner")


class Movement(Base):
    __tablename__ = "movements"
    
    movement_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="a_movement")
    description = Column(String, default="")
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    status = Column(String, default="started")
    start = Column(DateTime, default=datetime.now())
    stop = Column(DateTime, default = None)

    owner = relationship("User", back_populates="movements")