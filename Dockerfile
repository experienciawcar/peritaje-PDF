FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractiv
ENV PYTHONUNBUFFERED=1

# Install wkhtmltopdf and its dependencies
# Instalar dependencias necesarias en un solo paso
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xfonts-75dpi \
    xfonts-base \
    libjpeg-turbo8 \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    libssl3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Set working directory and copy application code
WORKDIR /
COPY . .

# Expone el puerto si usas Flask o similar
EXPOSE 8080

CMD ["python3", "app.py"]