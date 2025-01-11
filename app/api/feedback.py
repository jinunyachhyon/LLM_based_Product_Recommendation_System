from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/feedback/", response_model=schemas.FeedbackResponse)
def submit_feedback(feedback: schemas.FeedbackCreate, user_id: int, db: Session = Depends(get_db)):
    # Check if the user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the product exists
    product = db.query(models.Product).filter(models.Product.id == feedback.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Save feedback
    db_feedback = models.Feedback(
        user_id=user_id,
        product_id=feedback.product_id,
        rating=feedback.rating,
        comment=feedback.comment,
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
