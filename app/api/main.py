from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.user_route import router as user_router
from app.api.routes.file_upload_route import router as upload_router
from app.api.routes.stats_route import router as stats_router
from app.core.database import postgres_client


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Менеджер жизненного цикла приложения (Lifespan)"""

    await postgres_client.connect()

    yield

    await postgres_client.disconnect()

app = FastAPI(
    title="Archery Bot API",
    description="API для бота по учету тренировок в стрельбе из лука.",
    version="1.0.0",
    lifespan=app_lifespan)


app.include_router(user_router)
app.include_router(upload_router)
app.include_router(stats_router)
