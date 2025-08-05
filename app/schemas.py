# app/schemas.py mejorado
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    price: Decimal = Field(..., ge=0, decimal_places=2, description="Precio del producto")
    stock: int = Field(..., ge=0, description="Cantidad en stock")
    category: str = Field(..., min_length=1, max_length=50, description="Categoría del producto")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)

class ProductSchema(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop Gaming",
                "price": "999.99",
                "stock": 10,
                "category": "Electronics",
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }