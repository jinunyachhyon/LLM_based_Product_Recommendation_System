import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from bcrypt import hashpw, gensalt

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password
    hashed_password = hashpw(user.password.encode("utf-8"), gensalt())
    preferences_json = json.dumps(user.preferences) if user.preferences else None

    # Create the user
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password.decode("utf-8"),
        preferences=preferences_json,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
