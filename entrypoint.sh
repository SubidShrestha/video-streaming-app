#!/bin/sh
set -e

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL at $PG_HOST:$PG_PORT..."
until nc -z "$PG_HOST" "$PG_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL is up!"

# Run DB migrations
echo "🛠️  Running migrations..."
python3 manage.py migrate --noinput

echo "🛠️ Collecting staticfiles..."
python3 manage.py collectstatic --noinput

# Start Celery worker (in background)
echo "🌱 Starting Celery worker..."
celery -A video_streaming worker --loglevel=info &

# Start Gunicorn
echo "🚀 Starting Gunicorn server..."
exec gunicorn video_streaming.wsgi:application \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --timeout 30 \
  --access-logfile '-' \
  --error-logfile '-'