#!/bin/bash

set -e

# Запуск синхронизации папок, если указаны переменные окружения
if [ ! -z "$MOUNTED_DB_FOLDER" ]; then
    echo "Starting background sync folders..."
    ./background-sync-folders.sh /app/db "$MOUNTED_DB_FOLDER"
fi

# Ожидаем, пока база данных будет доступна (если это необходимо)
# echo "Waiting for database..."
# while ! python manage.py migrate --check; do
#     sleep 1
# done

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating admin user..."
python manage.py create-admin-user

echo "Starting Django server..."
exec "$@"