from decimal import Decimal
from typing import Optional
from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository
from ...shared.exceptions.domain_exceptions import ProductNotFoundError, ProductUpdateError

class UpdateProductUseCase:
    """Caso de uso para actualizar un producto"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(
        self, 
        product_id: int, 
        name: Optional[str] = None,
        price: Optional[float] = None,
        stock: Optional[int] = None,
        category: Optional[str] = None
    ) -> Product:
        """
        Ejecuta el caso de uso para actualizar un producto
        
        Args:
            product_id: ID del producto a actualizar
            name: Nuevo nombre (opcional)
            price: Nuevo precio (opcional)
            stock: Nuevo stock (opcional)
            category: Nueva categoría (opcional)
            
        Returns:
            Product: Producto actualizado
            
        Raises:
            ProductNotFoundError: Si el producto no existe
            ProductUpdateError: Si hay un error al actualizar
        """
        try:
            # Buscar el producto existente
            existing_product = self.product_repository.find_by_id(product_id)
            if not existing_product:
                raise ProductNotFoundError(f"Producto con ID {product_id} no encontrado")
            
            # Aplicar actualizaciones usando métodos de la entidad
            if name is not None:
                existing_product.update_name(name)
            
            if price is not None:
                existing_product.update_price(Decimal(str(price)))
            
            if stock is not None:
                existing_product.update_stock(stock)
            
            if category is not None:
                existing_product.update_category(category)
            
            # Guardar los cambios
            return self.product_repository.save(existing_product)
            
        except (ProductNotFoundError, ValueError) as e:
            # Re-lanzar errores de dominio
            raise e
        except Exception as e:
            # Error general
            raise ProductUpdateError(f"Error al actualizar producto: {str(e)}")

class PurchaseProductUseCase:
    """Caso de uso para realizar una compra de producto"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, product_id: int, quantity: int) -> Product:
        """
        Ejecuta el caso de uso para realizar una compra
        
        Args:
            product_id: ID del producto
            quantity: Cantidad a comprar
            
        Returns:
            Product: Producto actualizado después de la compra
            
        Raises:
            ProductNotFoundError: Si el producto no existe
            ProductUpdateError: Si hay un error al actualizar
        """
        try:
            # Buscar el producto
            product = self.product_repository.find_by_id(product_id)
            if not product:
                raise ProductNotFoundError(f"Producto con ID {product_id} no encontrado")
            
            # Realizar la compra usando lógica de dominio
            product.purchase(quantity)
            
            # Guardar los cambios
            return self.product_repository.save(product)
            
        except (ProductNotFoundError, ValueError) as e:
            # Re-lanzar errores de dominio
            raise e
        except Exception as e:
            # Error general
            raise ProductUpdateError(f"Error al realizar compra: {str(e)}")

class RestockProductUseCase:
    """Caso de uso para reabastecer un producto"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, product_id: int, quantity: int) -> Product:
        """
        Ejecuta el caso de uso para reabastecer un producto
        
        Args:
            product_id: ID del producto
            quantity: Cantidad a agregar al stock
            
        Returns:
            Product: Producto actualizado después del reabastecimiento
            
        Raises:
            ProductNotFoundError: Si el producto no existe
            ProductUpdateError: Si hay un error al actualizar
        """
        try:
            # Buscar el producto
            product = self.product_repository.find_by_id(product_id)
            if not product:
                raise ProductNotFoundError(f"Producto con ID {product_id} no encontrado")
            
            # Reabastecer usando lógica de dominio
            product.restock(quantity)
            
            # Guardar los cambios
            return self.product_repository.save(product)
            
        except (ProductNotFoundError, ValueError) as e:
            # Re-lanzar errores de dominio
            raise e
        except Exception as e:
            # Error general
            raise ProductUpdateError(f"Error al reabastecer producto: {str(e)}") 