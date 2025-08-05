from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Product:
    """Entidad de dominio Product - Contiene la lógica de negocio"""
    id: Optional[int]
    name: str
    price: Decimal
    stock: int
    category: str
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validaciones de dominio que se ejecutan después de la inicialización"""
        self._validate()
    
    def _validate(self):
        """Validaciones de dominio"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("El nombre del producto no puede estar vacío")
        
        if len(self.name) > 100:
            raise ValueError("El nombre del producto no puede exceder 100 caracteres")
        
        if self.price < 0:
            raise ValueError("El precio no puede ser negativo")
        
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        if not self.category or len(self.category.strip()) == 0:
            raise ValueError("La categoría no puede estar vacía")
        
        if len(self.category) > 50:
            raise ValueError("La categoría no puede exceder 50 caracteres")
    
    def update_stock(self, new_stock: int):
        """Lógica de negocio para actualizar stock"""
        if new_stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        self.stock = new_stock
        self.updated_at = datetime.now()
    
    def update_price(self, new_price: Decimal):
        """Lógica de negocio para actualizar precio"""
        if new_price < 0:
            raise ValueError("El precio no puede ser negativo")
        
        self.price = new_price
        self.updated_at = datetime.now()
    
    def update_name(self, new_name: str):
        """Lógica de negocio para actualizar nombre"""
        if not new_name or len(new_name.strip()) == 0:
            raise ValueError("El nombre del producto no puede estar vacío")
        
        if len(new_name) > 100:
            raise ValueError("El nombre del producto no puede exceder 100 caracteres")
        
        self.name = new_name.strip()
        self.updated_at = datetime.now()
    
    def update_category(self, new_category: str):
        """Lógica de negocio para actualizar categoría"""
        if not new_category or len(new_category.strip()) == 0:
            raise ValueError("La categoría no puede estar vacía")
        
        if len(new_category) > 50:
            raise ValueError("La categoría no puede exceder 50 caracteres")
        
        self.category = new_category.strip()
        self.updated_at = datetime.now()
    
    def is_available(self) -> bool:
        """Lógica de negocio para verificar disponibilidad"""
        return self.stock > 0
    
    def is_low_stock(self, threshold: int = 10) -> bool:
        """Lógica de negocio para verificar stock bajo"""
        return self.stock <= threshold
    
    def can_purchase(self, quantity: int) -> bool:
        """Lógica de negocio para verificar si se puede comprar"""
        return self.stock >= quantity and quantity > 0
    
    def purchase(self, quantity: int):
        """Lógica de negocio para realizar una compra"""
        if not self.can_purchase(quantity):
            raise ValueError(f"No se puede comprar {quantity} unidades. Stock disponible: {self.stock}")
        
        self.stock -= quantity
        self.updated_at = datetime.now()
    
    def restock(self, quantity: int):
        """Lógica de negocio para reabastecer stock"""
        if quantity <= 0:
            raise ValueError("La cantidad de reabastecimiento debe ser positiva")
        
        self.stock += quantity
        self.updated_at = datetime.now()
    
    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock})" 