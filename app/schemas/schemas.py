from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.models import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductBase(BaseModel):
    sku: str
    name: str
    category: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class InventoryBase(BaseModel):
    current_stock: int
    min_stock: int
    max_stock: int

class ProductResponse(ProductBase):
    id: int
    inventory: Optional[InventoryBase] = None
    class Config:
        from_attributes = True

class SalesCreate(BaseModel):
    product_id: int
    quantity: int
    date: Optional[datetime] = None

class PredictionResponse(BaseModel):
    product_id: int
    sku: str
    days_until_stockout: float
    status: str
