from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    preferences: Optional[dict] = None  # Preferences as a dictionary

class UserResponse(BaseModel):
    id: int
    username: str
    preferences: Optional[dict]

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str

    class Config:
        orm_mode = True