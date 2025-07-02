import uvicorn
import sys
from fastapi import FastAPI
from pathlib import Path
from contextlib import asynccontextmanager


sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.uslugi import router as router_uslugi
from src.api.bookings import router as router_bookings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    yield
    # При выключении/перезагрузке приложения
    await redis_manager.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_uslugi)
app.include_router(router_bookings)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)