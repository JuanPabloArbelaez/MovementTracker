import hashlib
from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    encoded_password = user.password.encode("utf-8")
    hashed_password = hashlib.sha256(encoded_password).hexdigest()
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_movements(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Movement).offset(skip).limit(limit).all()


def get_active_movement(db: Session, user_id: int):
    return db.query(models.Movement).\
        filter(models.Movement.owner_id == user_id).\
        filter(models.Movement.status == "started").first()


def start_movement(db: Session, movement: schemas.MovementStart, user_id: int):
    db_item = models.Movement(**movement.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


#TODO: Change status of movement object
def stop_movement():
    pass


