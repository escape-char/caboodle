import pytest
import json
from typing import Final
from unittest.mock import patch, MagicMock
from backend.common.cache import init, get_cache, Cache
from backend.settings import settings
from backend.common.utils import get_conn_str

name: Final[str] = "redis-cache"


async def return_value(n=None):
    return MagicMock(name=(n or name))


async def async_return(value):
    return value


@pytest.fixture(scope='function')
async def mock_cache():
    with patch('backend.common.cache.aioredis') as mock_redis:
        mock_redis.create_pool.return_value = return_value()
        yield await init()


@patch('backend.common.cache.aioredis')
class TestCache:
    @pytest.mark.asyncio
    async def test_init(self, mock_redis):
        mock_redis.create_pool.return_value = return_value()
        cache = await init()
        args = mock_redis.create_pool.call_args

        assert (
            args[0][0] == 'redis://localhost:6379' and
            args[1]["password"] is None and
            args[1]["ssl"] is False
        )

        assert cache._extract_mock_name() == name

    @pytest.mark.asyncio
    async def test_get_cache(self, mock_redis):
        mock_redis.create_pool.return_value = return_value()
        cache = await get_cache()
        args = mock_redis.create_pool.call_args

        assert cache.cache._extract_mock_name() == name
        assert args[0][0] == get_conn_str(
            settings.redis_protocol,
            settings.redis_host,
            settings.redis_port,
            db=settings.redis_db
        )
        assert args[1]["password"] is None and args[1]["ssl"] is False

        # calling multiple times should get existing cache and not reinitialize
        await get_cache()
        await get_cache()

        assert mock_redis.create_pool.call_count == 1

    def test_Cache_init(self, mock_redis, mock_cache):
        cache: Cache = Cache(mock_cache)
        assert cache.cache._extract_mock_name() == name

    @pytest.mark.asyncio
    async def test_Cache_get_json(self, mock_redis, mock_cache):
        json_dict = dict(key1="value1")
        key: Final[str] = "key"
        mock_cache.get.return_value = async_return(json.dumps(json_dict))
        cache: Cache = Cache(mock_cache)

        result = await cache.get(key)

        assert result == json_dict
        assert mock_cache.get.called_with(key)

    @pytest.mark.asyncio
    async def test_Cache_get(self, mock_redis, mock_cache):
        d = dict(key1="value1")
        key: Final[str] = "key"
        mock_cache.get.return_value = async_return(d)
        cache: Cache = Cache(mock_cache)

        result = await cache.get(key, use_json=False)

        assert result == d
        mock_cache.get.assert_called_with(key)

    @pytest.mark.asyncio
    async def test_Cache_set_json(self, mock_redis, mock_cache):
        key: Final[str] = "key"
        value: Final[str] = dict(key1="value1")
        expire: Final[int] = 300
        cache: Cache = Cache(mock_cache)

        mock_cache.set.return_value = async_return(None)

        await cache.set(key, value, expire)

        mock_cache.set.assert_called_with(
            key,
            json.dumps(value),
            expire
        )

    @pytest.mark.asyncio
    async def test_Cache_set(self, mock_redis, mock_cache):
        key: Final[str] = "key"
        value: Final[str] = dict(key1="value1")
        expire: Final[int] = 300
        cache: Cache = Cache(mock_cache)

        mock_cache.set.return_value = async_return(None)

        await cache.set(key, value, expire, use_json=False)

        mock_cache.set.assert_called_with(
            key,
            value,
            expire
        )

    @pytest.mark.asyncio
    async def test_Cache_delete(self, mock_redis, mock_cache):
        key: Final[str] = "key"
        cache: Cache = Cache(mock_cache)

        mock_cache.delete.return_value = async_return(None)
        await cache.delete(key)

        mock_cache.delete.assert_called_with(key)
