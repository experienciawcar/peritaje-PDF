FROM python:3.10-slim-bullseye

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    wget \
    xfonts-75dpi \
    xfonts-base \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libcairo2-dev \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
 && rm -rf /var/lib/apt/lists/*

# Instalar wkhtmltopdf desde .deb oficial (buster, compatible con bullseye)
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
 && apt-get install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb \
 && rm wkhtmltox_0.12.6-1.buster_amd64.deb

# Establecer directorio de trabajo
WORKDIR /

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Puerto para Cloud Run
EXPOSE 8080

# Comando de inicio
CMD ["python", "app.py"]
