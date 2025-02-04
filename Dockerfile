FROM python:3.9-slim

WORKDIR /app

# Instala las dependencias necesarias para compilar psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copia las dependencias
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del backend
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
