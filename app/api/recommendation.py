from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
import json

router = APIRouter()

@router.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    # Fetch user by ID
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Deserialize user preferences
    user_preferences = json.loads(user.preferences) if user.preferences else {}

    # Get category preference
    preferred_category = user_preferences.get("category")
    if not preferred_category:
        raise HTTPException(status_code=400, detail="No preferences found for user")

    # Fetch products matching the category
    products = db.query(models.Product).filter(models.Product.category == preferred_category).all()

    return {"user_id": user_id, "preferred_category": preferred_category, "products": products}
