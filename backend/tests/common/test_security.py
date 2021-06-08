import pytest
from unittest.mock import MagicMock, patch
from typing import Final, List, Optional
from backend.common.security import utils, constants
from backend.common.schema import (
    AccessTokenData,
    User,
    Permission,
    Role
)
from backend.settings import settings
from backend.common.utils import min_from_now


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


def test_password_hash():
    password: Final[str] = "testpass"

    with patch('backend.common.security.utils.pwd_context') as pcontext:
        return_value: Final[str] = "secrethash"
        pcontext.hash = MagicMock(return_value=return_value)
        hash = utils.gen_password_hash(password)

        pcontext.hash.assert_called_with(password)
        assert hash == return_value


def test_verify_password():
    password: Final[str] = "testpass"
    hash: Final[str] = utils.gen_password_hash(password)

    assert utils.verify_password(password, hash)


@pytest.mark.asyncio
async def test_encode_token():
    data: AccessTokenData = AccessTokenData(
        sub="userid1",
        name="john doe",
        email="john.doe@test.not",
        given_username="john.doe",
        iss="test issuer"
    )

    with patch(
        'backend.common.security.utils.jwt',
    ) as mock_jwt:
        return_val: Final[str] = "generatedtoken"
        mock_jwt.encode = MagicMock(return_value=return_val)

        result: dict = await utils.encode_access_token(data)
        args = mock_jwt.encode.call_args

        # verify encode is called with correct data
        assert (
            args[0][0]['sub'] == data.sub and
            args[0][0]['name'] == data.name and
            args[0][0]['email'] == data.email and
            args[0][0]['given_username'] == data.given_username and
            args[0][0]['iss'] == data.iss
        )

        # verify expiration is set correctly
        exp1: Final[str] = str(
            min_from_now(settings.auth_expire)
        ).split(".")[0]
        exp2: Final[str] = str(args[0][0]["exp"]).split(".")[0]
        assert exp1 == exp2

        # verify auth algorithm and secret key is passed
        assert args[0][1] == settings.auth_secret_key
        assert args[1]["algorithm"] == settings.auth_algorithm

        # verify response
        assert result["token"] == return_val
        assert str(result["expires_at"]).split(".")[0] == exp1


@pytest.mark.asyncio
async def test_decode_token():
    data: AccessTokenData = AccessTokenData(
        sub="userid1",
        name="john doe",
        email="john.doe@test.not",
        given_username="john.doe",
        iss="test issuer"
    )
    encode_result: dict = await utils.encode_access_token(data)

    with patch(
        'backend.common.security.utils.jwt',
    ) as mock_jwt:
        return_val: Final[str] = data.copy().dict()
        mock_jwt.decode = MagicMock(return_value=return_val)

        result: dict = await utils.decode_access_token(encode_result["token"])

        args = mock_jwt.decode.call_args

        # verify decode is called with correct data
        assert (
            args[0][0] == encode_result["token"] and
            args[0][1] == settings.auth_secret_key and
            args[1]["algorithms"] == [settings.auth_algorithm]
        )

        assert result == return_val


def test_has_access_valid(valid_user_roles):
    resource: Final[str] = constants.Resource.BOOKMARKS
    roles: Final[List[str]] = [constants.Role.BOOKMARKS_ADMINISTRATOR]

    assert utils.has_access(valid_user_roles, resource, roles)


def test_has_access_invalid_resource(valid_user_roles):
    resource: Final[str] = "invalidresource"
    roles: Final[List[str]] = [constants.Role.BOOKMARKS_ADMINISTRATOR]
    exception: Optional[Exception] = None

    try:
        utils.has_access(valid_user_roles, resource, roles)
    except ValueError as e:
        exception = e

    assert isinstance(exception, ValueError)
    assert str(exception) == utils.ERROR_INVALID_RESOURCE


def test_has_access_invalid_roles(valid_user_roles):
    resource: Final[str] = constants.Resource.BOOKMARKS
    roles: Final[List[str]] = ["invalid_role"]
    exception: Optional[Exception] = None

    try:
        utils.has_access(valid_user_roles, resource, roles)
    except ValueError as e:
        exception = e

    assert isinstance(exception, ValueError)
    assert str(exception) == utils.ERROR_INVALID_ROLE


def test_has_access_no_access(valid_user_roles):
    user: User = User(**valid_user_roles.dict())
    user.roles = []
    resource: Final[str] = constants.Resource.BOOKMARKS
    roles: Final[List[str]] = [constants.Role.BOOKMARKS_ADMINISTRATOR]

    assert not utils.has_access(user, resource, roles)
