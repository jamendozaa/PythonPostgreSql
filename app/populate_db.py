# app/populate_db.py mejorado
from sqlalchemy.orm import Session
from faker import Faker
import random
import os
import sys

# Agregar el directorio padre al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Product

def create_sample_products(db: Session, num_products: int = 1000):
    fake = Faker(['es_ES'])  # Datos en español
    
    categories = ["Electronics", "Books", "Clothing", "Home", "Toys", "Sports", "Beauty", "Automotive"]
    
    for _ in range(num_products):
        product = Product(
            name=fake.word().capitalize() + " " + fake.word().capitalize(),
            price=round(random.uniform(5, 500), 2),
            stock=random.randint(0, 100),
            category=random.choice(categories)
        )
        db.add(product)
    
    db.commit()
    print(f"✅ {num_products} productos creados exitosamente.")

if __name__ == "__main__":
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Poblar base de datos
    db = SessionLocal()
    try:
        create_sample_products(db)
    finally:
        db.close()