# app/main.py mejorado
from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from .database import SessionLocal, engine, Base, get_db
from .models import Product
from .schemas import ProductSchema, ProductCreate, ProductUpdate
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Product API",
    description="API para gestión de productos",
    version="1.0.0"
)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Productos"}

@app.get("/check-db", tags=["Health"])
def check_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Conexión exitosa con la base de datos"}
    except Exception as e:
        logger.error(f"Error de conexión a BD: {e}")
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

@app.get("/products", response_model=List[ProductSchema], tags=["Products"])
def get_products(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    products = query.offset(skip).limit(limit).all()
    return products

@app.get("/products/categories", tags=["Products"])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Product.category).distinct().all()
    return {"categories": [cat[0] for cat in categories]}

@app.get("/products/{product_id}", response_model=ProductSchema, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.post("/products", response_model=ProductSchema, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=ProductSchema, tags=["Products"])
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Producto eliminado exitosamente"}