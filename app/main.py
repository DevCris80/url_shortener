from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

def get_application() -> FastAPI:
    application = FastAPI(
        title="URL Shortener API",
        version="1.0.0",
        lifespan=lifespan
    )
    application.include_router(api_router, prefix="/api/v1")
    return application

app = get_application()

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API", "docs": "/docs"}