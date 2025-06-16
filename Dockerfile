#Python образ
FROM python:3.13-slim

# Установка записимосте 
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#Рабочая дерикрория внутри контейнера
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

#Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# переходим в каталог с manage.py
WORKDIR /app/VideoTestProject

# Команда для запуска окружения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

