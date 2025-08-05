# PythonPostgreSql - Arquitectura Limpia

Una aplicación FastAPI con PostgreSQL implementada usando **Arquitectura Limpia (Clean Architecture)** o **Arquitectura de Cebolla**.

## 🧅 Arquitectura Limpia

### **¿Qué es la Arquitectura Limpia?**

La Arquitectura Limpia es un patrón arquitectónico que organiza el código en **capas concéntricas**, donde cada capa tiene responsabilidades específicas y las dependencias apuntan hacia adentro (hacia el dominio).

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA CEBOLLA                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    PRESENTATION                        │ │
│  │                 (Controllers/API)                      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    APPLICATION                          │ │
│  │                (Use Cases/Services)                    │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                      DOMAIN                            │ │
│  │                (Entities/Business Rules)               │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  INFRASTRUCTURE                        │ │
│  │              (Database/External APIs)                  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Estructura del Proyecto

```
PythonPostgreSql/
├── app/
│   ├── domain/                    # 🧅 Capa de Dominio (más interna)
│   │   ├── entities/              # Entidades de negocio
│   │   │   └── product.py         # Entidad Product con lógica de negocio
│   │   └── repositories/          # Interfaces de repositorios
│   │       └── product_repository.py
│   │
│   ├── application/               # 🧅 Capa de Aplicación
│   │   └── use_cases/             # Casos de uso
│   │       ├── create_product.py
│   │       ├── get_products.py
│   │       ├── update_product.py
│   │       └── delete_product.py
│   │
│   ├── infrastructure/            # 🧅 Capa de Infraestructura (más externa)
│   │   ├── database/              # Configuración de BD
│   │   │   ├── connection.py
│   │   │   └── models.py
│   │   └── repositories/          # Implementaciones de repositorios
│   │       └── sql_product_repository.py
│   │
│   ├── presentation/              # 🧅 Capa de Presentación
│   │   ├── controllers/           # Controladores HTTP
│   │   │   └── product_controller.py
│   │   ├── schemas/               # Esquemas Pydantic
│   │   │   └── product_schemas.py
│   │   └── main.py                # Aplicación FastAPI
│   │
│   └── shared/                    # 🧅 Código compartido
│       └── exceptions/            # Excepciones personalizadas
│           └── domain_exceptions.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── populate_db.py                 # Script actualizado
└── README.md
```

## 🎯 Beneficios de la Arquitectura Limpia

### **✅ Ventajas Técnicas:**
1. **Independencia de frameworks**: El dominio no depende de FastAPI o SQLAlchemy
2. **Testabilidad**: Cada capa se puede probar independientemente
3. **Mantenibilidad**: Cambios aislados por capa
4. **Escalabilidad**: Fácil agregar nuevas funcionalidades

### **✅ Ventajas de Negocio:**
1. **Flexibilidad**: Cambiar tecnologías sin afectar el negocio
2. **Reutilización**: Casos de uso reutilizables
3. **Claridad**: Responsabilidades bien definidas
4. **Evolución**: Fácil evolución del sistema

## 🔧 Componentes de la Arquitectura

### **1. Capa de Dominio (Domain Layer)**

**Responsabilidades:**
- ✅ Entidades de negocio
- ✅ Reglas de negocio
- ✅ Interfaces de repositorios
- ✅ Excepciones de dominio

**Ejemplo:**
```python
# app/domain/entities/product.py
@dataclass
class Product:
    id: Optional[int]
    name: str
    price: Decimal
    stock: int
    category: str
    
    def purchase(self, quantity: int):
        """Lógica de negocio para realizar una compra"""
        if not self.can_purchase(quantity):
            raise ValueError(f"No se puede comprar {quantity} unidades")
        self.stock -= quantity
```

### **2. Capa de Aplicación (Application Layer)**

**Responsabilidades:**
- ✅ Casos de uso
- ✅ Orquestación de operaciones
- ✅ Validaciones de aplicación

**Ejemplo:**
```python
# app/application/use_cases/create_product.py
class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, name: str, price: float, stock: int, category: str) -> Product:
        product = Product(id=None, name=name, price=price, stock=stock, category=category)
        return self.product_repository.save(product)
```

### **3. Capa de Infraestructura (Infrastructure Layer)**

**Responsabilidades:**
- ✅ Implementaciones concretas
- ✅ Configuración de base de datos
- ✅ Servicios externos

**Ejemplo:**
```python
# app/infrastructure/repositories/sql_product_repository.py
class SQLProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, product: Product) -> Product:
        # Implementación con SQLAlchemy
        pass
```

### **4. Capa de Presentación (Presentation Layer)**

**Responsabilidades:**
- ✅ Controladores HTTP
- ✅ Esquemas de validación
- ✅ Manejo de requests/responses

**Ejemplo:**
```python
# app/presentation/controllers/product_controller.py
@router.post("/products")
def create_product(
    product_data: ProductCreateRequest,
    product_repository: SQLProductRepository = Depends(get_product_repository)
):
    use_case = CreateProductUseCase(product_repository)
    product = use_case.execute(
        name=product_data.name,
        price=float(product_data.price),
        stock=product_data.stock,
        category=product_data.category
    )
    return ProductResponse.from_orm(product)
```

## 🚀 Instalación y Uso

### **1. Clonar y configurar**
```bash
git clone https://github.com/Ale-Mendoza-07/PythonPostgreSql.git
cd PythonPostgreSql
```

### **2. Levantar con Docker**
```bash
docker-compose up -d
```

### **3. Poblar base de datos**
```bash
docker-compose run populate
```

### **4. Acceder a la API**
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Arquitectura**: http://localhost:8000/architecture

## 📊 Endpoints de la API

### **Endpoints Básicos**
- `GET /` - Información de la aplicación
- `GET /health` - Verificación de salud
- `GET /check-db` - Verificación de base de datos
- `GET /architecture` - Información de la arquitectura

### **Endpoints de Productos**
- `GET /api/v1/products` - Listar productos
- `GET /api/v1/products/{id}` - Obtener producto
- `POST /api/v1/products` - Crear producto
- `PUT /api/v1/products/{id}` - Actualizar producto
- `DELETE /api/v1/products/{id}` - Eliminar producto

### **Endpoints Avanzados**
- `GET /api/v1/products/categories` - Obtener categorías
- `GET /api/v1/products/low-stock` - Productos con stock bajo
- `POST /api/v1/products/{id}/purchase` - Realizar compra
- `POST /api/v1/products/{id}/restock` - Reabastecer

## 🧪 Testing

### **Ventajas de Testing con Arquitectura Limpia:**

1. **Testing de Dominio:**
```python
def test_product_purchase():
    product = Product(id=1, name="Test", price=10.0, stock=5, category="Test")
    product.purchase(2)
    assert product.stock == 3
```

2. **Testing de Casos de Uso:**
```python
def test_create_product_use_case():
    mock_repository = MockProductRepository()
    use_case = CreateProductUseCase(mock_repository)
    product = use_case.execute("Test", 10.0, 5, "Test")
    assert product.name == "Test"
```

3. **Testing de Controladores:**
```python
def test_create_product_endpoint():
    response = client.post("/api/v1/products", json={
        "name": "Test",
        "price": "10.0",
        "stock": 5,
        "category": "Test"
    })
    assert response.status_code == 201
```

## 🔄 Flujo de Datos

```
1. Request HTTP → 2. Controller → 3. Use Case → 4. Domain Entity → 5. Repository → 6. Database
     ↓              ↓              ↓              ↓                ↓              ↓
FastAPI        Validation      Business      Business         SQLAlchemy    PostgreSQL
             (Pydantic)       Logic         Rules           (Infra)       (Infra)
```

## 🎯 Principios Aplicados

### **1. Dependency Inversion Principle**
- Las capas internas no dependen de las externas
- Las dependencias apuntan hacia adentro

### **2. Single Responsibility Principle**
- Cada clase tiene una responsabilidad específica
- Separación clara de responsabilidades

### **3. Open/Closed Principle**
- Abierto para extensión, cerrado para modificación
- Nuevas funcionalidades sin cambiar código existente

### **4. Interface Segregation Principle**
- Interfaces específicas para cada necesidad
- No dependencias innecesarias

## 🚀 Próximos Pasos

### **Mejoras Sugeridas:**
1. **Implementar tests unitarios** para cada capa
2. **Agregar autenticación JWT** con casos de uso
3. **Implementar cache** con Redis
4. **Agregar logging estructurado**
5. **Implementar event sourcing**
6. **Agregar CQRS** (Command Query Responsibility Segregation)

### **Escalabilidad:**
1. **Microservicios** separados por dominio
2. **Message queues** para comunicación asíncrona
3. **API Gateway** para routing
4. **Service Mesh** para comunicación entre servicios

## 📚 Recursos Adicionales

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Implementa siguiendo la Arquitectura Limpia
4. Agrega tests para tu funcionalidad
5. Abre un Pull Request

---

**¡Disfruta explorando la Arquitectura Limpia! 🧅✨** 