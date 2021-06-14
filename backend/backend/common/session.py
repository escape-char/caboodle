from typing import Final
from fastapi import Request
from backend.common.cache import Cache
from backend.common.schema import User
from backend.common.constants import SESSION_KEY, SESSION_EXPIRE


def get_ip(request: Request) -> str:
    return request.client


def _get_key(token: str, ip: str) -> str:
    return SESSION_KEY % (token, ip)


async def get_session(cache: Cache, token: str, ip: str) -> User:
    user_json: Final[dict] = await cache.get(_get_key(token, ip))

    if not user_json:
        return None

    return User(**user_json)


async def set_session(cache: Cache, session: User, token: str, ip: str):
    cache.set(
        _get_key(token, ip),
        session.dict(),
        SESSION_EXPIRE
    )


async def remove_session(cache: Cache, token: str, ip: str):
    cache.delete(_get_key(token, ip))
