from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, db_engine


models.Base.metadata.create_all(bind=db_engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
    finally:
        db.close()


@app.get("/")
def index():
    return("Movement Tracker V0")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/movements/", response_model=schemas.Movement)
def create_movement_for_user(
    user_id: int, movement: schemas.MovementStart, db: Session = Depends(get_db)
):
    return crud.start_movement(db=db, movement=movement, user_id=user_id)


@app.get("/movements/", response_model=list[schemas.Movement])
def get_movements(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    movements = crud.get_movements(db=db, skip=skip, limit=limit)
    return movements






