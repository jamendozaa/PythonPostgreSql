import psycopg2
from faker import Faker
import random
import os

# Leer credenciales desde variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydb")

# Parsear la URL (opción simple para psycopg2)
import re
pattern = r"postgresql://(.*?):(.*?)@(.*?):(.*?)/(.*)"
match = re.match(pattern, DATABASE_URL)
db_user, db_pass, db_host, db_port, db_name = match.groups()

# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_pass,
    host=db_host,
    port=db_port
)
cursor = conn.cursor()
fake = Faker()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10,2),
    stock INTEGER,
    category TEXT,
    created_at TIMESTAMP
);
""")

# Insertar 1000 productos falsos
for _ in range(1000):
    name = fake.word().capitalize()
    price = round(random.uniform(5, 500), 2)
    stock = random.randint(0, 100)
    category = random.choice(["Electronics", "Books", "Clothing", "Home", "Toys"])
    created_at = fake.date_time_this_year()
    cursor.execute("""
        INSERT INTO products (name, price, stock, category, created_at)
        VALUES (%s, %s, %s, %s, %s);
    """, (name, price, stock, category, created_at))

conn.commit()
cursor.close()
conn.close()
print("✅ Base de datos poblada con éxito.")
