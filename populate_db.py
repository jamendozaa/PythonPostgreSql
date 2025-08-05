#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de prueba.
Este script utiliza la nueva Arquitectura Limpia.
"""

import sys
import os

# Agregar el directorio app al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.infrastructure.database.connection import engine, Base
from app.infrastructure.database.models import ProductModel
from app.domain.entities.product import Product
from app.application.use_cases.create_product import CreateProductUseCase
from app.infrastructure.repositories.sql_product_repository import SQLProductRepository
from app.infrastructure.database.connection import SessionLocal
from faker import Faker
import random

def create_sample_products(num_products: int = 1000):
    """Crea productos de muestra usando la Arquitectura Limpia."""
    fake = Faker(['es_ES'])  # Datos en español
    
    categories = ["Electronics", "Books", "Clothing", "Home", "Toys", "Sports", "Beauty", "Automotive"]
    
    print(f"Creando {num_products} productos usando Arquitectura Limpia...")
    
    # Crear sesión de base de datos
    db = SessionLocal()
    try:
        # Crear repositorio
        product_repository = SQLProductRepository(db)
        
        # Crear caso de uso
        create_product_use_case = CreateProductUseCase(product_repository)
        
        for i in range(num_products):
            try:
                # Crear producto usando el caso de uso
                product = create_product_use_case.execute(
                    name=fake.word().capitalize() + " " + fake.word().capitalize(),
                    price=round(random.uniform(5, 500), 2),
                    stock=random.randint(0, 100),
                    category=random.choice(categories)
                )
                
                # Mostrar progreso cada 100 productos
                if (i + 1) % 100 == 0:
                    print(f"Progreso: {i + 1}/{num_products} productos creados")
                    
            except Exception as e:
                print(f"Error al crear producto {i + 1}: {e}")
                continue
        
        print(f"✅ {num_products} productos creados exitosamente usando Arquitectura Limpia.")
        
    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {e}")
        raise
    finally:
        db.close()

def main():
    """Función principal del script."""
    print("🚀 Iniciando población de base de datos con Arquitectura Limpia...")
    
    try:
        # Crear tablas si no existen
        print("📋 Creando tablas...")
        Base.metadata.create_all(bind=engine)
        
        # Poblar base de datos
        print("📊 Poblando base de datos...")
        create_sample_products()
        
        print("🎉 ¡Base de datos poblada exitosamente con Arquitectura Limpia!")
        
    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 