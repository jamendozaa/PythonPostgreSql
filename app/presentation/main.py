from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

# Controladores
from .controllers.product_controller import router as product_router

# Base de datos
from ..infrastructure.database.connection import get_db_session

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Product API - Clean Architecture",
    description="API para gestión de productos implementada con Arquitectura Limpia",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir routers
app.include_router(product_router, prefix="/api/v1", tags=["Products"])

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz de la aplicación"""
    return {
        "message": "Bienvenido a la API de Productos con Arquitectura Limpia",
        "version": "2.0.0",
        "architecture": "Clean Architecture (Onion)",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de verificación de salud de la aplicación"""
    return {
        "status": "healthy",
        "message": "La aplicación está funcionando correctamente"
    }

@app.get("/check-db", tags=["Health"])
def check_database(db: Session = Depends(get_db_session)):
    """Verificar conexión a la base de datos"""
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "message": "Conexión exitosa con la base de datos",
            "architecture": "Clean Architecture"
        }
    except Exception as e:
        logger.error(f"Error de conexión a BD: {e}")
        return {
            "status": "error",
            "message": f"Error de conexión a la base de datos: {str(e)}"
        }

@app.get("/architecture", tags=["Info"])
def get_architecture_info():
    """Información sobre la arquitectura del proyecto"""
    return {
        "architecture": "Clean Architecture (Onion)",
        "layers": {
            "presentation": "Controladores y esquemas Pydantic",
            "application": "Casos de uso y servicios",
            "domain": "Entidades y reglas de negocio",
            "infrastructure": "Implementaciones concretas (BD, APIs externas)"
        },
        "benefits": [
            "Independencia de frameworks",
            "Testabilidad mejorada",
            "Mantenibilidad",
            "Escalabilidad",
            "Separación de responsabilidades"
        ],
        "principles": [
            "Dependency Inversion",
            "Single Responsibility",
            "Open/Closed Principle",
            "Interface Segregation"
        ]
    } 