from pydantic import BaseModel
from datetime import datetime

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str
    created_at: datetime

    class Config:
        orm_mode = True
