from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import update, delete
from database import engine, Base, get_db
from helper import get_one_user_by_id, validate_email
import models, schemas
from typing import List
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not validate_email(user.email):
        raise HTTPException(status_code=403, detail="Invalid Email")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_one_user_by_id(user_id, db)

@app.put("/users/{user_id}", response_model=int)
def update_user(user: schemas.UserUpdate, user_id: int, db: Session = Depends(get_db)):
    query = update(models.User).where(models.User.id == user_id).values(**user.dict())
    result = db.execute(query)
    db.commit()
    return result.rowcount
    

@app.delete("/users/{user_id}", response_model=int)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    get_one_user_by_id(user_id, db)
    query = delete(models.User).where(models.User.id == user_id)
    result = db.execute(query)
    db.commit()
    return result.rowcount

@app.get("/matches/{user_id}", response_model=List[schemas.User])
def get_matches(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    user = get_one_user_by_id(user_id, db)
    matched_users = db.query(models.User).filter(models.User.interests.contains(user.interests), models.User.city == user.city).offset(skip)\
        .limit(limit).all()
    return matched_users
