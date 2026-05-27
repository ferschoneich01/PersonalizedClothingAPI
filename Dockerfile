FROM python:3.10-alpine

WORKDIR /app

COPY . /app

# Instala dependencias del sistema necesarias
RUN apk update \
    && apk add --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    gdk-pixbuf-dev \
    cairo-dev \
    pango-dev \
    libc-dev \
    gobject-introspection-dev

# Instala paquetes críticos primero (antes de requirements.txt)
RUN pip install --no-cache-dir \
    gunicorn \
    flask \
    flask-cors \
    python-dotenv \
    psycopg2

# Instala el resto de dependencias (continúa aunque algún paquete opcional falle)
RUN pip3 --no-cache-dir install -r requirements.txt || \
    pip3 --no-cache-dir install -r requirements.txt --ignore-installed

WORKDIR /app/src

CMD [ "gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "app:app" ]
