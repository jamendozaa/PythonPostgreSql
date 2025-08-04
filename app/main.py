from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text  # ✅ Importar text
from .database import SessionLocal, engine, Base, get_db
from .models import Product
from .schemas import ProductSchema
from typing import List

app = FastAPI()

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

@app.get("/check-db")
def check_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  # ✅ Usar text()
        return {"status": "ok", "message": "Conexión exitosa con la base de datos"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/products", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
