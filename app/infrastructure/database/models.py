from sqlalchemy import Column, Integer, String, Numeric, DateTime, Index
from sqlalchemy.sql import func
from .connection import Base

class ProductModel(Base):
    """Modelo SQLAlchemy para la tabla products"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_product_category_price', 'category', 'price'),
        Index('idx_product_stock', 'stock'),
    )
    
    def __repr__(self):
        return f"<ProductModel(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock})>" 