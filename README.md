# PythonPostgreSql

Una aplicación FastAPI con PostgreSQL que incluye una API REST para gestionar productos.

##  Características

- **FastAPI**: Framework web moderno y rápido para Python
- **PostgreSQL**: Base de datos relacional robusta
- **SQLAlchemy**: ORM para Python
- **Docker Compose**: Orquestación de contenedores
- **PgAdmin**: Interfaz web para administrar PostgreSQL
- **Faker**: Generación de datos de prueba

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 🛠️ Instalación y Configuración

### Opción 1: Usando Docker (Recomendado)

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/Ale-Mendoza-07/PythonPostgreSql.git
   cd PythonPostgreSql
   ```

2. **Levanta los servicios con Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Verifica que todos los servicios estén funcionando**
   ```bash
   docker-compose ps
   ```

4. **Pobla la base de datos con datos de prueba**
   ```bash
   docker-compose run populate
   ```

### Opción 2: Instalación Local

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/Ale-Mendoza-07/PythonPostgreSql.git
   cd PythonPostgreSql
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura PostgreSQL localmente**
   - Instala PostgreSQL en tu sistema
   - Crea una base de datos llamada `mydb`
   - Crea un usuario `user` con contraseña `password`
   - O modifica la variable `DATABASE_URL` en `app/database.py`

5. **Ejecuta la aplicación**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Pobla la base de datos (opcional)**
   ```bash
   python app/populate_db.py
   ```

## 🌐 Acceso a los Servicios

Una vez que los servicios estén ejecutándose, podrás acceder a:

- **API FastAPI**: http://localhost:8000
- **Documentación automática**: http://localhost:8000/docs
- **PgAdmin**: http://localhost:5050
  - Email: `admin@admin.com`
  - Contraseña: `admin123`

## 📊 Endpoints de la API

- `GET /check-db`: Verifica la conexión con la base de datos
- `GET /products`: Obtiene todos los productos

## 🔧 Configuración de Variables de Entorno

El proyecto utiliza las siguientes variables de entorno:

- `DATABASE_URL`: URL de conexión a PostgreSQL
- `POSTGRES_USER`: Usuario de PostgreSQL (default: `user`)
- `POSTGRES_PASSWORD`: Contraseña de PostgreSQL (default: `password`)
- `POSTGRES_DB`: Nombre de la base de datos (default: `mydb`)

##  Estructura del Proyecto

```
PythonPostgreSql/
├── app/
│   ├── __init__.py
│   ├── database.py      # Configuración de la base de datos
│   ├── main.py          # Aplicación FastAPI principal
│   ├── models.py        # Modelos SQLAlchemy
│   ├── populate_db.py   # Script para poblar la BD
│   └── schemas.py       # Esquemas Pydantic
├── docker-compose.yml   # Configuración de Docker Compose
├── Dockerfile          # Imagen Docker para la aplicación
├── requirements.txt    # Dependencias de Python
└── README.md          # Este archivo
```

##  Solución de Problemas

### Error de conexión a la base de datos
- Verifica que PostgreSQL esté ejecutándose
- Confirma que las credenciales sean correctas
- Asegúrate de que el puerto 5432 esté disponible

### Error al ejecutar Docker Compose
- Verifica que Docker esté ejecutándose
- Asegúrate de que los puertos 8000, 5432 y 5050 estén libres
- Ejecuta `docker-compose down` y luego `docker-compose up -d`

### Problemas con las dependencias
- Elimina el entorno virtual y créalo nuevamente
- Actualiza pip: `pip install --upgrade pip`
- Instala las dependencias una por una si es necesario

## 🤝 Contribución

1. Fork el proyecto desde [https://github.com/Ale-Mendoza-07/PythonPostgreSql](https://github.com/Ale-Mendoza-07/PythonPostgreSql)
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🔗 Enlaces Útiles

- [Repositorio en GitHub](https://github.com/Ale-Mendoza-07/PythonPostgreSql)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de PostgreSQL](https://www.postgresql.org/docs/)
- [Documentación de SQLAlchemy](https://docs.sqlalchemy.org/)