#!/bin/sh

set -e

echo "=========================================="
echo "Waiting for PostgreSQL..."
echo "=========================================="

until pg_isready \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER"
do
    echo "PostgreSQL is unavailable - waiting..."
    sleep 2
done

echo "=========================================="
echo "PostgreSQL is ready."
echo "=========================================="

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ ! -d "chatbot/vector_store" ] || [ -z "$(ls -A chatbot/vector_store 2>/dev/null)" ]; then
    echo "Building RAG vector database..."
    python manage.py build_index_excel
else
    echo "RAG vector database already exists."
fi

echo "=========================================="
echo "Starting Gunicorn..."
echo "=========================================="

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers=${GUNICORN_WORKERS:-3}