from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.api import auth, product

# Create the FastAPI app instance
app = FastAPI()

# Initialize the database
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(product.router, prefix="/products", tags=["products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM-based Product Recommendation System!"}