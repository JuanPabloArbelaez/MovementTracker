import hashlib
from datetime import datetime

from sqlalchemy.orm import Session

import models, schemas
from schemas import MovementStatus



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    encoded_password = user.password.encode("utf-8")
    hashed_password = hashlib.sha256(encoded_password).hexdigest()
    username = user.email.split("@")[0]
    db_user = models.User(
        email=user.email,
        username=username,
        hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_movements(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Movement).offset(skip).limit(limit).all()


def get_active_movement(db: Session, username: str):
    return db.query(models.Movement).\
        filter(models.Movement.owner_username == username).\
        filter(models.Movement.status == MovementStatus.started).first()


def start_movement(db: Session, movement: schemas.MovementStart, username: str):
    db_item = models.Movement(**movement.dict(), owner_username=username)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def stop_movement(db: Session, username: str):
    active_movement = get_active_movement(db, username)
    if not active_movement:
        return None
    active_movement.stop = datetime.now()
    active_movement.status = MovementStatus.stopped
    db.commit()
    db.refresh(active_movement)
    return active_movement


