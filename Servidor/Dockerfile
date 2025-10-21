# Usa una imagen base ligera con Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos del proyecto al contenedor
COPY servidor_archivos.py .

# Instala dependencias si existen
RUN pip install --no-cache-dir -r requirements.txt || echo "No hay requirements"

# Expone el puerto que usa tu servidor
EXPOSE 5000

# Ejecuta el servidor
CMD ["python", "servidor_archivos.py"]

