from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.product import Product

class ProductRepository(ABC):
    """Interfaz del repositorio de productos - Define el contrato para acceder a datos"""
    
    @abstractmethod
    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto"""
        pass
    
    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Busca un producto por ID"""
        pass
    
    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene todos los productos con paginación"""
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[Product]:
        """Busca productos por categoría"""
        pass
    
    @abstractmethod
    def find_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Busca productos por rango de precio"""
        pass
    
    @abstractmethod
    def find_low_stock(self, threshold: int = 10) -> List[Product]:
        """Busca productos con stock bajo"""
        pass
    
    @abstractmethod
    def find_available(self) -> List[Product]:
        """Busca productos disponibles (stock > 0)"""
        pass
    
    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Elimina un producto por ID"""
        pass
    
    @abstractmethod
    def get_categories(self) -> List[str]:
        """Obtiene todas las categorías disponibles"""
        pass
    
    @abstractmethod
    def count_by_category(self, category: str) -> int:
        """Cuenta productos por categoría"""
        pass 