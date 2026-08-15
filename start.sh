#!/bin/bash
set -e

echo "Waiting for database connection..."
python -c "
import time, psycopg2, os
db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/telecom_db')
for i in range(30):
    try:
        psycopg2.connect(db_url)
        print('Database connected successfully!')
        break
    except Exception as e:
        print('Waiting for database...')
        time.sleep(1)
"

echo "Running database migrations..."
alembic upgrade head

echo "Starting Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
