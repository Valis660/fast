from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.init import redis_manager
from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.uslugi import router as router_uslugi
from src.api.bookings import router as router_bookings
from src.api.images import router as router_images


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()

    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    # При выключении/перезагрузке приложения
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

# Добавляем CORS middleware перед роутерами
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_uslugi)
app.include_router(router_bookings)
app.include_router(router_images)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
