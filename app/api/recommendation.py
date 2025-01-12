from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.utils.llm import LLMRecommender
import json

# Initialize the router
router = APIRouter()

# Initialize the embedding-based LLM recommender
llm_recommender = LLMRecommender(model_name="all-MiniLM-L6-v2")  # A lightweight sentence-transformer model

@router.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    # Step 1: Fetch the user and validate
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Deserialize user preferences
    user_preferences = json.loads(user.preferences) if user.preferences else {}
    preferred_category = user_preferences.get("category")
    price_range = user_preferences.get("price_range", [0, float("inf")])
    if not preferred_category:
        raise HTTPException(status_code=400, detail="No preferences found for user")

    # Step 2: Fetch products matching the preferred category
    products = db.query(models.Product).filter(models.Product.category == preferred_category).all()
    if not products:
        return {"user_id": user_id, "message": "No products found for the preferred category"}

    # Step 3: Prepare preferences and product descriptions for ranking
    preferences_text = f"User preferences: {json.dumps(user_preferences)}"
    product_descriptions = [f"{p.name}: {p.description}" for p in products]

    # Step 4: Use the embedding-based LLM to rank products
    ranked_products = llm_recommender.rank_products(preferences_text, product_descriptions)

    # Step 5: Format the ranked products for the response
    response_products = []
    for product_text in ranked_products:
        product_name = product_text.split(":")[0]  # Extract product name
        matching_product = next((p for p in products if p.name == product_name), None)
        if matching_product:
            response_products.append(
                {
                    "id": matching_product.id,
                    "name": matching_product.name,
                    "description": matching_product.description,
                    "price": matching_product.price,
                    "category": matching_product.category,
                }
            )

    return {
        "user_id": user_id,
        "preferred_category": preferred_category,
        "ranked_products": response_products,
    }