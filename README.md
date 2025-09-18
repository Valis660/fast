# Hotel Booking System

Полнофункциональная система бронирования отелей с современным веб-интерфейсом и REST API.

## 🏗️ Архитектура

Проект состоит из двух основных частей:

- **Backend** - FastAPI приложение с PostgreSQL и Redis
- **Frontend** - React приложение с TypeScript и Tailwind CSS

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Git

### Запуск всего проекта

1. **Создайте Docker сеть:**
```bash
docker network create myNetwork
```

2. **Запустите базу данных и кэш:**
```bash
# PostgreSQL
docker run --name booking_db 
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg_booking_data:/var/lib/postgresql/data \
    -d postgres:16

# Redis
docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4
```

3. **Запустите все сервисы через Docker Compose:**
```bash
docker-compose up --build
```

### Доступ к приложению

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 📋 Функциональность

### 🔐 Аутентификация
- Регистрация и вход пользователей
- JWT токены для авторизации
- Защищенные маршруты

### 🏨 Управление отелями
- CRUD операции для отелей
- Поиск и фильтрация отелей
- Управление номерами и услугами

### 📅 Система бронирования
- Бронирование номеров на даты
- Расчет стоимости бронирования
- Просмотр личных бронирований

### ⚙️ Дополнительные возможности
- Кэширование с Redis
- Асинхронные задачи с Celery
- Миграции базы данных
- Тестирование

## 🛠️ Технологический стек

### Backend
- **FastAPI** - современный веб-фреймворк
- **PostgreSQL** - основная база данных
- **Redis** - кэширование и сессии
- **SQLAlchemy** - ORM
- **Alembic** - миграции
- **Celery** - асинхронные задачи
- **Pydantic** - валидация данных

### Frontend
- **React 18** - UI библиотека
- **TypeScript** - типизация
- **Tailwind CSS** - стилизация
- **React Query** - управление состоянием
- **React Router** - маршрутизация
- **Axios** - HTTP клиент

### DevOps
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация
- **Nginx** - веб-сервер

## 📁 Структура проекта

```
├── src/                    # Backend код
│   ├── api/               # API endpoints
│   ├── models/            # ORM модели
│   ├── services/          # Бизнес-логика
│   ├── repositories/      # Работа с данными
│   ├── schemas/           # Pydantic схемы
│   └── tasks/             # Celery задачи
├── frontend/              # Frontend код
│   ├── src/
│   │   ├── components/    # React компоненты
│   │   ├── pages/         # Страницы
│   │   ├── api/           # API клиенты
│   │   └── contexts/      # React контексты
│   └── public/            # Статические файлы
├── tests/                 # Тесты
├── docker-compose.yaml    # Docker Compose конфигурация
└── README.md
```

## 🔧 Разработка

### Backend разработка

```bash
# Установка зависимостей
pip install -r req.txt

# Запуск миграций
alembic upgrade head

# Запуск сервера
uvicorn src.main:app --reload
```

### Frontend разработка

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск в режиме разработки
npm start
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием
pytest --cov=src

# Запуск только unit тестов
pytest tests/unit_tests/

# Запуск только integration тестов
pytest tests/integration_tests/
```

## 📚 API Документация

После запуска приложения документация API доступна по адресам:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🚀 Деплой

### Продакшен

```bash
# Сборка всех образов
docker-compose -f docker-compose.prod.yml build

# Запуск в продакшене
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 Лицензия

MIT License# fast
