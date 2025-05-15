FROM python:3.10-slim

# Cambia todos los mirrors de APT a uno alternativo más confiable
RUN find /etc/apt/ -name '*.list' -exec sed -i 's|http://deb.debian.org/debian|http://ftp.debian.org/debian|g' {} +

# Desactiva la validación de vigencia de los índices (ayuda con mirrors desincronizados)
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid

# Instalación robusta de dependencias del sistema con reintentos
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get update \
    && until apt-get install -y --no-install-recommends wkhtmltopdf xfonts-75dpi xfonts-base; do \
           echo "Reintentando instalación en 5 segundos..."; sleep 5; \
           apt-get update; \
       done \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto si usas Flask o similar
EXPOSE 8080

# El resto del código se montará como volumen
