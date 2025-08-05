from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class ProductCreateRequest(BaseModel):
    """Esquema para crear un producto"""
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    price: Decimal = Field(..., ge=0, decimal_places=2, description="Precio del producto")
    stock: int = Field(..., ge=0, description="Cantidad en stock")
    category: str = Field(..., min_length=1, max_length=50, description="Categoría del producto")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Laptop Gaming",
                "price": "999.99",
                "stock": 10,
                "category": "Electronics"
            }
        }

class ProductUpdateRequest(BaseModel):
    """Esquema para actualizar un producto"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del producto")
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Precio del producto")
    stock: Optional[int] = Field(None, ge=0, description="Cantidad en stock")
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="Categoría del producto")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Laptop Gaming Pro",
                "price": "899.99",
                "stock": 15
            }
        }

class ProductResponse(BaseModel):
    """Esquema para respuesta de producto"""
    id: int
    name: str
    price: Decimal
    stock: int
    category: str
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

class ProductPurchaseRequest(BaseModel):
    """Esquema para realizar una compra"""
    quantity: int = Field(..., gt=0, description="Cantidad a comprar")
    
    class Config:
        schema_extra = {
            "example": {
                "quantity": 2
            }
        }

class ProductRestockRequest(BaseModel):
    """Esquema para reabastecer un producto"""
    quantity: int = Field(..., gt=0, description="Cantidad a agregar al stock")
    
    class Config:
        schema_extra = {
            "example": {
                "quantity": 10
            }
        }

class ProductListResponse(BaseModel):
    """Esquema para lista de productos"""
    products: List[ProductResponse]
    total: int
    skip: int
    limit: int
    
    class Config:
        schema_extra = {
            "example": {
                "products": [
                    {
                        "id": 1,
                        "name": "Laptop Gaming",
                        "price": "999.99",
                        "stock": 10,
                        "category": "Electronics",
                        "created_at": "2024-01-01T10:00:00",
                        "updated_at": "2024-01-01T10:00:00"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 10
            }
        }

class CategoryResponse(BaseModel):
    """Esquema para respuesta de categorías"""
    categories: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "categories": ["Electronics", "Books", "Clothing", "Home"]
            }
        }

class MessageResponse(BaseModel):
    """Esquema para respuestas de mensaje"""
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Operación realizada exitosamente"
            }
        } 