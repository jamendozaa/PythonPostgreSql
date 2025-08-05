from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session

# Casos de uso
from ...application.use_cases.create_product import CreateProductUseCase
from ...application.use_cases.get_products import (
    GetProductsUseCase, 
    GetProductByIdUseCase, 
    GetProductCategoriesUseCase,
    GetLowStockProductsUseCase
)
from ...application.use_cases.update_product import (
    UpdateProductUseCase,
    PurchaseProductUseCase,
    RestockProductUseCase
)
from ...application.use_cases.delete_product import DeleteProductUseCase

# Repositorio
from ...infrastructure.repositories.sql_product_repository import SQLProductRepository

# Esquemas
from ..schemas.product_schemas import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse,
    ProductPurchaseRequest,
    ProductRestockRequest,
    ProductListResponse,
    CategoryResponse,
    MessageResponse
)

# Excepciones
from ...shared.exceptions.domain_exceptions import (
    ProductCreationError,
    ProductNotFoundError,
    ProductUpdateError,
    ProductDeletionError
)

# Base de datos
from ...infrastructure.database.connection import get_db_session

router = APIRouter()

def get_product_repository(session: Session = Depends(get_db_session)) -> SQLProductRepository:
    """Dependency injection para el repositorio de productos"""
    return SQLProductRepository(session)

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(
    product_data: ProductCreateRequest,
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    """Crear un nuevo producto"""
    try:
        use_case = CreateProductUseCase(product_repository)
        product = use_case.execute(
            name=product_data.name,
            price=float(product_data.price),
            stock=product_data.stock,
            category=product_data.category
        )
        
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            category=product.category,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
    except ProductCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products", response_model=List[ProductResponse], tags=["Products"])
def get_products(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    """Obtener productos con filtros y paginación"""
    use_case = GetProductsUseCase(product_repository)
    products = use_case.execute(
        skip=skip,
        limit=limit,
        category=category,
        min_price=min_price,
        max_price=max_price
    )
    
    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            category=product.category,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        for product in products
    ]

@router.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product(
    product_id: int,
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    """Obtener un producto por ID"""
    use_case = GetProductByIdUseCase(product_repository)
    product = use_case.execute(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return ProductResponse(
        id=product.id,
        name=product.name,
        price=product.price,
        stock=product.stock,
        category=product.category,
        created_at=product.created_at,
        updated_at=product.updated_at
    )

@router.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def update_product(
    product_id: int,
    product_data: ProductUpdateRequest,
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    """Actualizar un producto"""
    try:
        use_case = UpdateProductUseCase(product_repository)
        product = use_case.execute(
            product_id=product_id,
            name=product_data.name,
            price=float(product_data.price) if product_data.price else None,
            stock=product_data.stock,
            category=product_data.category
        )
        
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            category=product.category,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProductUpdateError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/products/{product_id}", response_model=MessageResponse, tags=["Products"])
def delete_product(
    product_id: int,
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    """Eliminar un producto"""
    try:
        use_case = DeleteProductUseCase(product_repository)
        use_case.execute(product_id)
        return MessageResponse(message="Producto eliminado exitosamente")
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProductDeletionError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products/categories", response_model=CategoryResponse, tags=["Products"])
def get_categories(
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    """Obtener todas las categorías disponibles"""
    use_case = GetProductCategoriesUseCase(product_repository)
    categories = use_case.execute()
    return CategoryResponse(categories=categories)

@router.get("/products/low-stock", response_model=List[ProductResponse], tags=["Products"])
def get_low_stock_products(
    threshold: int = Query(10, ge=0, description="Umbral de stock bajo"),
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    """Obtener productos con stock bajo"""
    use_case = GetLowStockProductsUseCase(product_repository)
    products = use_case.execute(threshold)
    
    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            category=product.category,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        for product in products
    ]

@router.post("/products/{product_id}/purchase", response_model=ProductResponse, tags=["Products"])
def purchase_product(
    product_id: int,
    purchase_data: ProductPurchaseRequest,
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    """Realizar una compra de producto"""
    try:
        use_case = PurchaseProductUseCase(product_repository)
        product = use_case.execute(product_id, purchase_data.quantity)
        
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            category=product.category,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProductUpdateError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/products/{product_id}/restock", response_model=ProductResponse, tags=["Products"])
def restock_product(
    product_id: int,
    restock_data: ProductRestockRequest,
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    """Reabastecer un producto"""
    try:
        use_case = RestockProductUseCase(product_repository)
        product = use_case.execute(product_id, restock_data.quantity)
        
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            category=product.category,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProductUpdateError as e:
        raise HTTPException(status_code=400, detail=str(e)) 