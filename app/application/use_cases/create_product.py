from datetime import datetime
from decimal import Decimal
from typing import Optional
from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository
from ...shared.exceptions.domain_exceptions import ProductCreationError

class CreateProductUseCase:
    """Caso de uso para crear un producto"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, name: str, price: float, stock: int, category: str) -> Product:
        """
        Ejecuta el caso de uso para crear un producto
        
        Args:
            name: Nombre del producto
            price: Precio del producto
            stock: Cantidad en stock
            category: Categoría del producto
            
        Returns:
            Product: Producto creado
            
        Raises:
            ProductCreationError: Si hay un error al crear el producto
        """
        try:
            # Crear entidad de dominio con validaciones
            product = Product(
                id=None,
                name=name,
                price=Decimal(str(price)),
                stock=stock,
                category=category,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Guardar usando el repositorio
            return self.product_repository.save(product)
            
        except ValueError as e:
            # Error de validación de dominio
            raise ProductCreationError(f"Error de validación: {str(e)}")
        except Exception as e:
            # Error general
            raise ProductCreationError(f"Error al crear producto: {str(e)}") 