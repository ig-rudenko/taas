import os
import pickle
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any

from redis.asyncio import Redis


cache_value_type = int | float | str | dict | list


class AbstractCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any | None:
        pass

    @abstractmethod
    async def set(self, key: str, value: cache_value_type, expire: int) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass


def singleton(cls):
    """Декоратор синглтона"""

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance

    return wrapper


@singleton
class InMemoryCache(AbstractCache):
    def __init__(self):
        self._cache = {}

    async def get(self, key: str) -> Any | None:
        try:
            return self._cache[key]
        except KeyError:
            return None

    async def set(self, key: str, value: cache_value_type, expire: int) -> None:
        self._cache[key] = value

    async def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    async def clear(self) -> None:
        self._cache.clear()


@singleton
class RedisCache(AbstractCache):
    def __init__(self, host: str, port: int, db: int) -> None:
        self._redis: Redis = Redis(host=host, port=port, db=db)

    async def get(self, key: str) -> Any | None:
        value = await self._redis.get(key)
        if value is not None:
            return pickle.loads(value)

    async def set(self, key: str, value: cache_value_type, expire: int) -> None:
        await self._redis.set(key, pickle.dumps(value), ex=expire)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def clear(self) -> None:
        await self._redis.flushdb(asynchronous=True)


@singleton
class CacheService(AbstractCache):
    def __init__(self):
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        redis_port = int(os.environ.get("REDIS_PORT", 6379))
        redis_db = int(os.environ.get("REDIS_DB", 3))
        if redis_host and redis_port and redis_db and False:
            self._cache: AbstractCache = RedisCache(redis_host, redis_port, redis_db)
        else:
            self._cache: AbstractCache = InMemoryCache()

    async def get(self, key: str) -> Any | None:
        return await self._cache.get(key)

    async def set(self, key: str, value: cache_value_type, expire: int) -> None:
        return await self._cache.set(key, value, expire)

    async def delete(self, key: str) -> None:
        return await self._cache.delete(key)

    async def clear(self) -> None:
        return await self._cache.clear()
