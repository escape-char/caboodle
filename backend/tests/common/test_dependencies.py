import pytest
from typing import Final, Optional, List
from fastapi import HTTPException, status
from unittest.mock import patch, MagicMock
from backend.common import dependencies
from backend.common.schema import AccessTokenData, User, Permission, Role
from backend.common.session import _get_key
from backend.common.security import constants


async def return_value(value):
    return value


@pytest.fixture
def valid_user_roles():
    role_name: Final[str] = constants.Role.BOOKMARKS_ADMINISTRATOR
    permissions = constants.role_to_perms[role_name]
    permissions = [Permission(
        id=1,
        name=p,
        resource_id=0,
        description=constants.permission_descr[p]
    ) for p in permissions]

    roles = [
        Role(
            id=2,
            name=role_name,
            resource_id=0,
            description=constants.role_descr[role_name],
            permissions=permissions
        )
    ]

    return User(
        id=12,
        username="test_user",
        name="test user",
        email="test_user@testing.not",
        roles=roles
    )


def test_get_db():
    name_db: Final[str] = "SessionLocal()"

    with patch('backend.common.dependencies.SessionLocal') as mock_session:
        db = dependencies.get_db()

        for d in db:
            mock_session.assert_called_once()
            assert d._extract_mock_name() == name_db

        mock_session().close.assert_called_once()


@pytest.mark.asyncio
async def test_get_cache():
    name_db: Final[str] = "get_cache_db()"
    with patch('backend.common.dependencies.get_cache_db') as mock_cache:
        cache = await dependencies.get_cache()

        mock_cache.assert_called_once()
        assert cache._extract_mock_name() == name_db


@pytest.mark.asyncio
async def test_token_data(user_jwt):
    data: AccessTokenData = await dependencies.get_token_data(user_jwt)
    assert isinstance(data, AccessTokenData)


@pytest.mark.asyncio
async def test_bad_token_data(user_jwt):
    token: Final[str] = "badtokendata"
    exception: Optional[Exception] = None

    try:
        await dependencies.get_token_data(token)
    except HTTPException as e:
        exception = e

    assert isinstance(exception, HTTPException)
    assert exception.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_user_session(user_jwt):
    name_req: Final[str] = "mock-request"
    name_cache: Final[str] = "mock-cache"
    ip: Final[str] = "127.0.0.1"
    request = MagicMock(name=name_req)
    cache = MagicMock(name=name_cache)
    data: AccessTokenData = await dependencies.get_token_data(user_jwt)

    user: User = User(
        id=22,
        username="test_user",
        email="test_user@testing.not",
        name="test user",
        roles=[]
    )
    request.client = ip

    cache.get.return_value = return_value(user.dict())

    user_session: User = await dependencies.get_user_session(
        request=request,
        token=user_jwt,
        token_data=data,
        cache=cache
    )
    args = cache.get.call_args

    assert args[0][0] == _get_key(user_jwt, ip)
    assert user_session.dict() == user.dict()


def test_check_access(valid_user_roles):
    with patch('backend.common.dependencies.has_access') as mock_access:
        mock_access.return_value = True
        resource: Final[str] = constants.Resource.BOOKMARKS
        roles: Final[List[str]] = [constants.Role.BOOKMARKS_ADMINISTRATOR]

        check_access = dependencies.CheckAccess(
            session=valid_user_roles,
            resource=resource,
            roles=roles,
        )

        success: bool = check_access.__call__()
        args = mock_access.call_args[0]

        assert success
        assert args[0].dict() == valid_user_roles.dict()
        assert args[1] == resource and args[2] == roles


def test_check_access_invalid(valid_user_roles):
    user: User = User(**valid_user_roles.dict())
    user.roles = []
    resource: Final[str] = constants.Resource.BOOKMARKS
    roles: Final[List[str]] = [constants.Role.BOOKMARKS_ADMINISTRATOR]
    exception: Optional[Exception] = None

    with patch('backend.common.dependencies.has_access') as mock_access:
        mock_access.return_value = False
        check_access = dependencies.CheckAccess(
            session=user,
            resource=resource,
            roles=roles,
        )

        try:
            check_access.__call__()
        except HTTPException as e:
            exception = e

        assert isinstance(exception, HTTPException)
        assert exception.status_code == status.HTTP_403_FORBIDDEN
