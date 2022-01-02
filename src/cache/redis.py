# coding=utf-8
import logging
import aioredis
from aioredis import Redis

from src.core.config import settings

__author__ = 'qPham'
_logger = logging.getLogger(__name__)


async def redis_pool():
    # aioredis.from_url creates a Redis client
    # backed by a pool of connections.
    redis = aioredis.from_url(
        settings.REDIS_HOST,
        encoding="utf8",
        decode_responses=True
    )
    return redis


def client(request) -> Redis:
    return request.app.state.redis
