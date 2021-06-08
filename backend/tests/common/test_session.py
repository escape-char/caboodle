from typing import Final
from uuid import uuid4
from unittest.mock import MagicMock
from backend.common import session
from backend.common.constants import SESSION_KEY, SESSION_EXPIRE
from backend.common.schema import User

import pytest

ip: Final[str] = "127.0.0.1"
token: Final[str] = str(uuid4())


async def return_value(value):
    return value


@pytest.fixture(scope='function')
async def mock_redis():
    return MagicMock()


@pytest.fixture(scope='function')
def mock_user():
    return User(
        id=22,
        username="testuser",
        email="testuser@test.not",
        name="test user",
        roles=[]
    )


def test_get_key():
    assert(session._get_key(token, ip) == SESSION_KEY % (token, ip))


def test_get_ip():
    request = MagicMock()
    request.client = ip
    assert session.get_ip(request) == request.client


@pytest.mark.asyncio
async def test_get_session(mock_redis, mock_user):
    mock_redis.get.return_value = return_value(mock_user.dict())

    user: User = await session.get_session(mock_redis, token, ip)

    mock_redis.get.assert_called_with(session._get_key(token, ip))

    assert user.dict() == mock_user.dict()


@pytest.mark.asyncio
async def test_set_session(mock_redis, mock_user):
    await session.set_session(
        mock_redis,
        mock_user,
        token,
        ip
    )
    mock_redis.set.assert_called_with(
        session._get_key(token, ip),
        mock_user.dict(),
        SESSION_EXPIRE
    )


@pytest.mark.asyncio
async def test_remove_session(mock_redis):
    await session.remove_session(
        mock_redis,
        token,
        ip
    )
    mock_redis.delete.assert_called_with(
        session._get_key(token, ip),
    )
