from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MovementStatus(str, Enum):
    started = "started"
    stopped = "stopped"
    error = "error"


class MovementKind(str, Enum):
    squat = "squat"
    walk = "walk"
    hang = "hang"
    goggins = "goggins"
    cycle = "cycle"
    interval = "interval"
    meditate = "meditate"
    multi = "multi"


class MovementBase(BaseModel):
    kind: MovementKind
    title: str = "a_movement"
    description: str = ""
    status: MovementStatus
    start: datetime = datetime.now()
    stop: datetime | None


class MovementStart(MovementBase):
    status: MovementStatus = MovementStatus.started
    kind: MovementKind = MovementKind.squat
    stop: datetime | None = None


class MovementStop(MovementBase):
    stop: datetime | None = None
    status: MovementStatus = MovementStatus.stopped


class Movement(MovementBase):
    movement_id: int
    owner_username: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str | None = None


class UserCreate(UserBase):
    password: str
    username: str | None = None


class User(UserBase):
    user_id: int
    is_active: bool
    movements: list[MovementBase] = []

    class Config:
        orm_mode = True

