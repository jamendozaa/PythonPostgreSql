from ...domain.repositories.product_repository import ProductRepository
from ...shared.exceptions.domain_exceptions import ProductNotFoundError, ProductDeletionError

class DeleteProductUseCase:
    """Caso de uso para eliminar un producto"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, product_id: int) -> bool:
        """
        Ejecuta el caso de uso para eliminar un producto
        
        Args:
            product_id: ID del producto a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            ProductNotFoundError: Si el producto no existe
            ProductDeletionError: Si hay un error al eliminar
        """
        try:
            # Verificar que el producto existe
            existing_product = self.product_repository.find_by_id(product_id)
            if not existing_product:
                raise ProductNotFoundError(f"Producto con ID {product_id} no encontrado")
            
            # Eliminar el producto
            success = self.product_repository.delete(product_id)
            
            if not success:
                raise ProductDeletionError(f"No se pudo eliminar el producto con ID {product_id}")
            
            return True
            
        except ProductNotFoundError:
            # Re-lanzar error de dominio
            raise
        except Exception as e:
            # Error general
            raise ProductDeletionError(f"Error al eliminar producto: {str(e)}") 