#Python образ
FROM python:3.13-slim

# Установка записимосте 
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && rm -rf /var/lib/apt/lists/*

#Рабочая дерикрория внутри контейнера
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

#Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Копируем и делаем исполняемым entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# переходим в каталог с manage.py
WORKDIR /app/VideoTestProject

# Запускаем entrypoint
ENTRYPOINT ["/entrypoint.sh"]

