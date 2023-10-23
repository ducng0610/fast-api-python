"""Main app"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from app.config import app_config
from app.db import database
from app.routers.parcel import router as parcel_router
from app.routers.train import router as train_router
from app.routers.trainline import router as trainline_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(parcel_router, tags=["Parcel"])
app.include_router(train_router, tags=["Train"])
app.include_router(trainline_router, tags=["Train Line"])


@app.get("/ping")
def pong():
    return {
        "status": "ok",
        "environment": app_config.ENV_STATE,
        "testing": app_config.TESTING,
    }


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
