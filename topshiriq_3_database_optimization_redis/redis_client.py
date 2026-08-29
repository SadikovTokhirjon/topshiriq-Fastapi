import os
import time
from typing import Optional, Any
import redis.asyncio as aioredis


class InMemoryAsyncRedis:
    """
    Agar lokal Redis server ishga tushmagan bo'lsa yoki testlar uchun
    ishlaydigan to'liq asinxron InMemory Redis kesh mexanizmi.
    """

    def __init__(self):
        self._store: dict[str, tuple[str, Optional[float]]] = {}

    async def get(self, key: str) -> Optional[str]:
        if key in self._store:
            val, expire_at = self._store[key]
            if expire_at is not None and time.time() > expire_at:
                del self._store[key]
                return None
            return val
        return None

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        expire_at = (time.time() + ex) if ex else None
        self._store[key] = (value, expire_at)
        return True

    async def delete(self, *keys: str) -> int:
        count = 0
        for k in keys:
            if k in self._store:
                del self._store[k]
                count += 1
        return count

    async def flushdb(self) -> bool:
        self._store.clear()
        return True

    async def ping(self) -> bool:
        return True


REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")


class RedisManager:
    """Haqiqiy Redis va InMemory Redis fallback boshqaruvchisi."""

    def __init__(self, url: str = REDIS_URL):
        self.url = url
        self._client = None
        self._is_fallback = False

    async def get_client(self):
        if self._client is not None:
            return self._client

        try:
            real_client = aioredis.from_url(
                self.url,
                decode_responses=True,
                socket_timeout=1.0,
                socket_connect_timeout=1.0,
            )
            # Ulanishni sinab ko'ramiz
            await real_client.ping()
            self._client = real_client
            self._is_fallback = False
            return self._client
        except Exception:
            # Agar Redis server topilmasa, InMemory keshga o'tiladi
            self._client = InMemoryAsyncRedis()
            self._is_fallback = True
            return self._client


# Global Redis klienti
redis_manager = RedisManager()


async def get_redis_client():
    """Asinxron Redis mijozini qaytarish."""
    return await redis_manager.get_client()
