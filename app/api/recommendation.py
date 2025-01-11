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
    preferred_category = user_preferences.get("category")
    price_range = user_preferences.get("price_range", [0, float("inf")])
    preferred_brands = user_preferences.get("brands", [])

    if not preferred_category:
        raise HTTPException(status_code=400, detail="User preferences are incomplete")

    # Fetch products matching the category
    products = db.query(models.Product).filter(models.Product.category == preferred_category).all()

    if not products:
        return {"user_id": user_id, "message": "No products found for the preferred category"}

    # Scoring function
    def score_product(product, user_id, db):
        score = 0
        feedback = db.query(models.Feedback).filter(models.Feedback.product_id == product.id).all()

        # Base score for price and brand match
        if product.price >= price_range[0] and product.price <= price_range[1]:
            score += 1
        if any(brand.lower() in product.name.lower() for brand in preferred_brands):
            score += 2

        # Adjust score based on average product rating
        if feedback:
            avg_rating = sum(f.rating for f in feedback) / len(feedback)
            score += avg_rating  # Higher rating increases score

        return score

    # Rank products by score
    scored_products = [{"product": product, "score": score_product(product, user_id, db)} for product in products]
    ranked_products = sorted(scored_products, key=lambda x: x["score"], reverse=True)

    # Format the response
    recommendations = [
        {
            "id": p["product"].id,
            "name": p["product"].name,
            "description": p["product"].description,
            "price": p["product"].price,
            "category": p["product"].category,
            "score": p["score"],
        }
        for p in ranked_products
    ]

    return {
        "user_id": user_id,
        "preferred_category": preferred_category,
        "recommendations": recommendations,
    }