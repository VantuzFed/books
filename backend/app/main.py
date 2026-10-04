from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import books

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при запуске: пробуем создать таблицы
    try:
        await init_db()
        logger.info("Подключение к MariaDB успешно, таблицы инициализированы.")
    except Exception as e:
        logger.warning(
            f"Не удалось подключиться к базе данных при запуске: {e}. "
            "Убедитесь, что MariaDB запущена и настройки в .env верны."
        )
    yield
    # Действия при остановке (graceful shutdown)


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Разрешаем CORS для интеграции с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров API
app.include_router(books.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    """Проверка доступности сервиса."""
    return {"status": "ok"}
