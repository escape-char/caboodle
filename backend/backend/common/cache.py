from typing import Optional, Any
import json
import aioredis
from backend.common.utils import get_conn_str
from backend.settings import settings


async def init(
    host: str = "localhost",
    port: int = 6379,
    db: int = 0,
    password: Optional[str] = None,
    ssl: bool = False
) -> aioredis.Redis:
    conn_str: str = get_conn_str(
        settings.redis_protocol,
        host,
        port,
        db=db
    )
    return await aioredis.create_pool(
        conn_str, password=password, ssl=ssl
    )


class Cache:
    def __init__(self, cache: aioredis.Redis):
        self.cache: aioredis.Redis = cache

    async def get(self, key: str, use_json: bool = True) -> Any:
        data: Any = await self.cache.get(key)
        return json.loads(data) if use_json and data is not None else data

    async def set(
        self,
        key: str,
        value: Any,
        expire: int = 0,
        use_json: bool = True
    ):
        data = json.dumps(value) if use_json else value
        await self.cache.set(key, data, expire)

    async def delete(
        self,
        key: str
    ):
        await self.cache.delete(key)


_cache: Optional[Cache] = None


async def get_cache() -> Cache:
    global _cache
    if not _cache:
        redis: aioredis.Redis = await init(
            settings.redis_host,
            settings.redis_port,
            settings.redis_db,
            settings.redis_password,
            settings.redis_ssl
        )
        _cache = Cache(redis)

    return _cache
