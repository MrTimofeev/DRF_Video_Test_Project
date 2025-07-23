# VideoTestProject

Проект реализует REST API для работы с видео: просмотр видео, постановка лайков, вывод статистики. Используется Django

## Основные возможности

- Получение списка видео и конкретного видео по ID
- Добавление и удаление лайков к видео
- Вывод статистики по лайкам пользователей
- Админ-панель для управления видео и пользователей
- Генерация тестовых данных

## Технологии

- Python 3.13
- Django 5.2
- Django REST Framework
- PostgreSQL
- Doker / docker-compose

---

## Установка и запуск черезе Doker

### 1. Клонируйте репозиторий:
``` bash
git clone https://github.com/MrTimofeev/DRF_Video_Test_Project.git
cd DRF_Video_Test_Project\VideoTestProject
```

### 2. Собери и запусти контейнеры:
``` bash
docker-compose up --build
```
Сервис будет доступен по адресу: `http://localhost:8000/v1/videos/`

### 3. Генерация тестовых данных

После запуска контейнера можно создать тестовые данные:
``` bash
docker-compose exec web python manage.py generate_test_data
```

Создаст:

- 10_000 пользователей
- По 10 видео на каждого пользователя (всего 100_000 видео)

## Локальная работа без Docker

### 1. Создай виртуальное окружение:
``` bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Установи зависимости:
``` bash 
pip install -r requirements.txt
```

### 3. Настрой PostgreSQL и обнови `settings.py` 

### 4. Примени миграции:

``` bash
python manage.py migrate
```

### 5. Запусти сервер:
``` bash
python manage.py runserver
```

