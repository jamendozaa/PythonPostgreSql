from typing import List, Optional
from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository

class GetProductsUseCase:
    """Caso de uso para obtener productos"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        """
        Ejecuta el caso de uso para obtener productos
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros
            category: Filtrar por categoría
            min_price: Precio mínimo
            max_price: Precio máximo
            
        Returns:
            List[Product]: Lista de productos
        """
        # Validar parámetros
        if skip < 0:
            skip = 0
        
        if limit < 1:
            limit = 100
        elif limit > 1000:
            limit = 1000
        
        # Aplicar filtros
        if category:
            return self.product_repository.find_by_category(category)
        
        if min_price is not None and max_price is not None:
            return self.product_repository.find_by_price_range(min_price, max_price)
        
        # Obtener todos los productos
        return self.product_repository.find_all(skip, limit)

class GetProductByIdUseCase:
    """Caso de uso para obtener un producto por ID"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, product_id: int) -> Optional[Product]:
        """
        Ejecuta el caso de uso para obtener un producto por ID
        
        Args:
            product_id: ID del producto
            
        Returns:
            Optional[Product]: Producto encontrado o None
        """
        if product_id <= 0:
            return None
        
        return self.product_repository.find_by_id(product_id)

class GetProductCategoriesUseCase:
    """Caso de uso para obtener categorías de productos"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self) -> List[str]:
        """
        Ejecuta el caso de uso para obtener categorías
        
        Returns:
            List[str]: Lista de categorías
        """
        return self.product_repository.get_categories()

class GetLowStockProductsUseCase:
    """Caso de uso para obtener productos con stock bajo"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, threshold: int = 10) -> List[Product]:
        """
        Ejecuta el caso de uso para obtener productos con stock bajo
        
        Args:
            threshold: Umbral de stock bajo
            
        Returns:
            List[Product]: Lista de productos con stock bajo
        """
        if threshold < 0:
            threshold = 0
        
        return self.product_repository.find_low_stock(threshold) 