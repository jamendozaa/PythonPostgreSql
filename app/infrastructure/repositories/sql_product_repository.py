from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository
from ..database.models import ProductModel

class SQLProductRepository(ProductRepository):
    """Implementación SQL del repositorio de productos"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto"""
        if product.id is None:
            # Crear nuevo producto
            product_model = ProductModel(
                name=product.name,
                price=product.price,
                stock=product.stock,
                category=product.category,
                created_at=product.created_at,
                updated_at=product.updated_at
            )
            self.session.add(product_model)
            self.session.commit()
            self.session.refresh(product_model)
            
            return self._to_domain_entity(product_model)
        else:
            # Actualizar producto existente
            product_model = self.session.query(ProductModel).filter(ProductModel.id == product.id).first()
            if product_model:
                product_model.name = product.name
                product_model.price = product.price
                product_model.stock = product.stock
                product_model.category = product.category
                product_model.updated_at = product.updated_at
                self.session.commit()
                return self._to_domain_entity(product_model)
            return None
    
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Busca un producto por ID"""
        product_model = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product_model:
            return self._to_domain_entity(product_model)
        return None
    
    def find_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene todos los productos con paginación"""
        product_models = self.session.query(ProductModel).offset(skip).limit(limit).all()
        return [self._to_domain_entity(pm) for pm in product_models]
    
    def find_by_category(self, category: str) -> List[Product]:
        """Busca productos por categoría"""
        product_models = self.session.query(ProductModel).filter(ProductModel.category == category).all()
        return [self._to_domain_entity(pm) for pm in product_models]
    
    def find_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Busca productos por rango de precio"""
        product_models = self.session.query(ProductModel).filter(
            and_(ProductModel.price >= min_price, ProductModel.price <= max_price)
        ).all()
        return [self._to_domain_entity(pm) for pm in product_models]
    
    def find_low_stock(self, threshold: int = 10) -> List[Product]:
        """Busca productos con stock bajo"""
        product_models = self.session.query(ProductModel).filter(ProductModel.stock <= threshold).all()
        return [self._to_domain_entity(pm) for pm in product_models]
    
    def find_available(self) -> List[Product]:
        """Busca productos disponibles (stock > 0)"""
        product_models = self.session.query(ProductModel).filter(ProductModel.stock > 0).all()
        return [self._to_domain_entity(pm) for pm in product_models]
    
    def delete(self, product_id: int) -> bool:
        """Elimina un producto por ID"""
        product_model = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product_model:
            self.session.delete(product_model)
            self.session.commit()
            return True
        return False
    
    def get_categories(self) -> List[str]:
        """Obtiene todas las categorías disponibles"""
        categories = self.session.query(ProductModel.category).distinct().all()
        return [cat[0] for cat in categories]
    
    def count_by_category(self, category: str) -> int:
        """Cuenta productos por categoría"""
        return self.session.query(ProductModel).filter(ProductModel.category == category).count()
    
    def _to_domain_entity(self, product_model: ProductModel) -> Product:
        """Convierte un modelo SQLAlchemy a entidad de dominio"""
        return Product(
            id=product_model.id,
            name=product_model.name,
            price=product_model.price,
            stock=product_model.stock,
            category=product_model.category,
            created_at=product_model.created_at,
            updated_at=product_model.updated_at
        ) 