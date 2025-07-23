#!/bin/sh

# Ожидание доступности PostgreSQL
echo "Ожидание PostgreSQL на db:5432..."
while ! nc -z db 5432; do
  echo "PostgreSQL ещё не готово. Жду 1 секунду..."
  sleep 1
done
echo "PostgreSQL готово!"

# Применяем миграции
echo "Применение миграций..."
python /app/VideoTestProject/manage.py migrate --noinput

# Запускаем сервер
echo "Запуск Django сервера..."
exec python /app/VideoTestProject/manage.py runserver 0.0.0.0:8000