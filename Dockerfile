FROM python:3.10-alpine

WORKDIR /app

COPY . /app

# Instala dependencias necesarias
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
    gobject-introspection-dev \
    && pip install --no-cache-dir psycopg2

RUN pip3 --no-cache-dir install -r requirements.txt

WORKDIR /app/src

CMD [ "gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "app:app" ]