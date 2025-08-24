FROM python:3.10-buster

# Instala dependencias del sistema necesarias para wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xfonts-75dpi \
    xfonts-base \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libcairo2-dev \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /

# Copia e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto si usas Flask o similar
EXPOSE 8080

# Comando para iniciar la app (ajusta según tu framework)
CMD ["python", "app.py"]
