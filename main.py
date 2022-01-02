# coding=utf-8
import logging
import logging.config
from fastapi.security import OAuth2
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware
from src.api import api_router
from src.cache import redis
from src.core.config import settings
from src.core.limiter import limiter
from concurrent.futures.thread import ThreadPoolExecutor
from slowapi import _rate_limit_exceeded_handler

__author__ = 'qPham'
_logger = logging.getLogger(__name__)

logging.config.fileConfig(
    './config/logging.ini',
    disable_existing_loggers=False
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_STR}/openapi.json",
    docs_url=settings.API_DOCS,
    redoc_url=settings.API_REDOC
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
oautht2_schema = OAuth2()


@app.on_event('startup')
async def startup():
    app.state.redis = await redis.redis_pool()
    app.state.executor = ThreadPoolExecutor()


@app.on_event("shutdown")
async def close_redis():
    await app.state.redis.close()
    app.state.executor.shutdown()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_STR)
