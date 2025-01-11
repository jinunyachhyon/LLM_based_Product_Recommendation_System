from fastapi import FastAPI

# Create the FastAPI app instance
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM-based Product Recommendation System!"}