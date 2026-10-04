# FastAPI + SQLAlchemy 2.0 + MariaDB Template

Минималистичный асинхронный шаблон для бэкенда.

## 🚀 Быстрый старт

### 1. Запуск MariaDB (Docker)

Если у вас установлен Docker, базу данных можно поднять одной командой:

```bash
cd backend
docker compose up -d
```

Параметры подключения по умолчанию:
- **Хост**: `localhost:3306`
- **Пользователь**: `books_user`
- **Пароль**: `books_password`
- **База**: `books_db`

### 2. Установка зависимостей

Создайте и активируйте виртуальное окружение:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Файл `.env` уже создан на основе `.env.example`. При необходимости отредактируйте параметры БД:

```env
PROJECT_NAME="Books API"
DEBUG=True

DB_HOST=localhost
DB_PORT=3306
DB_USER=books_user
DB_PASSWORD=books_password
DB_NAME=books_db
```

### 4. Запуск сервера

```bash
uvicorn app.main:app --reload --port 8000
```

- Документация Swagger (OpenAPI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Альтернативная документация ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 📁 Структура проекта

```text
backend/
├── app/
│   ├── config.py         # Настройки приложения через pydantic-settings (.env)
│   ├── database.py       # Async engine, AsyncSession, get_db зависимость, Base
│   ├── main.py           # Инициализация FastAPI, CORS, lifespan, подключение роутеров
│   ├── models/           # SQLAlchemy 2.0 модели (Mapped, mapped_column)
│   │   └── book.py       # Пример модели Book
│   ├── schemas/          # Pydantic схемы (валидация входных и выходных данных)
│   │   └── book.py
│   └── routers/          # API эндпоинты (роуты)
│       └── books.py      # CRUD операции для Book
├── .env                  # Локальные переменные окружения
├── .env.example          # Шаблон переменных
├── .gitignore
├── docker-compose.yml    # MariaDB 11.4 контейнер
├── requirements.txt      # Зависимости
└── README.md
```

## 🛠 Как расширять

1. **Новая модель**: добавьте класс в `app/models/` с наследованием от `Base` из `app.database`.
2. **Новые схемы**: добавьте Pydantic-модели в `app/schemas/`.
3. **Новый роутер**: создайте модуль в `app/routers/` с использованием `APIRouter` и инъекцией сессии через `db: AsyncSession = Depends(get_db)`.
4. Подключите роутер в `app/main.py` через `app.include_router(...)`.
