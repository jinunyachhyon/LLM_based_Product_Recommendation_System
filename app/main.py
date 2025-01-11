from fastapi import FastAPI
from app.database import engine
from app.models import Base

# Create the FastAPI app instance
app = FastAPI()

# Initialize the database
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM-based Product Recommendation System!"}