from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MovementStatus(str, Enum):
    started = "started"
    stopped = "stopped"
    error = "error"


class MovementBase(BaseModel):
    title: str = "a_movement"
    description: str = ""
    status: MovementStatus
    start: datetime = datetime.now()
    stop: datetime | None = None


class MovementStart(MovementBase):
    status: MovementStatus = MovementStatus("started")


class Movement(MovementBase):
    movement_id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    is_active: bool
    movements: list[MovementBase] = []

    class Config:
        orm_mode = True

