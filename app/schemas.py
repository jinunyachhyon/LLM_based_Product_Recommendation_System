from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict
import json

class UserCreate(BaseModel):
    username: str
    password: str
    preferences: Optional[Dict] = None

class UserResponse(BaseModel):
    id: int
    username: str
    preferences: Optional[Dict] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        # Ensure preferences is deserialized into a dictionary
        if obj.preferences and isinstance(obj.preferences, str):
            obj.preferences = json.loads(obj.preferences)
        return super().from_orm(obj)

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
        from_attributes = True