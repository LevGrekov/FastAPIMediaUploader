from fastapi import FastAPI

from app.routers import files, health

app = FastAPI(
    title="Media Uploader API",
    description="API для загрузки и обработки медиафайлов",
    version="1.0.0"
)

app.include_router(files.router, prefix="/api", tags=["files"])
app.include_router(health.router, tags=["health"])
