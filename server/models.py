from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    movements = relationship("Movement", back_populates="owner")


class Movement(Base):
    __tablename__ = "movements"
    
    movement_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kind = Column(String, index=True, default="squat")
    title = Column(String, default="a_movement")
    description = Column(String, default="")
    owner_username = Column(String, ForeignKey("users.username"))
    status = Column(String, default="started")
    start = Column(DateTime, default=datetime.now())
    stop = Column(DateTime, default = None)

    owner = relationship("User", back_populates="movements")


class MovementKind(Base):
    __tablename__ = "movement_kinds"
    
    kind_id = Column(String, primary_key=True, index=True)
