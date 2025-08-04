# Imagen base: Python 3.10 (ligera)
FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app/ ./app

# Exponer puerto
EXPOSE 8000

# Ejecutar uvicorn como módulo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
