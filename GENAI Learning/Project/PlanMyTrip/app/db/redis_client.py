from redis.asyncio import Redis

from app.core.config import settings

_redis: Redis | None = None


async def connect_redis() -> Redis:

    global _redis

    if _redis is None:

        _redis = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

        await _redis.ping()

    return _redis


async def disconnect_redis():

    global _redis

    if _redis:

        await _redis.close()

        _redis = None