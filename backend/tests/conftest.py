from typing import Final
from unittest.mock import MagicMock
import pytest
from backend.app import app
from fastapi.testclient import TestClient
from backend.common.dependencies import get_db
from backend.common.security.utils import encode_access_token
from backend.common.schema import AccessTokenData


MOCK_DB_NAME: Final[str] = "mock-database"


def override_get_db():
    return MagicMock(name=MOCK_DB_NAME)


@pytest.fixture(scope="session")
def web_app_client():
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="function")
async def user_jwt():
    data: AccessTokenData = AccessTokenData(
        sub=22,
        name="test user",
        email="test_user@testing.not",
        given_username="test_user",
        iss="caboodle"
    )
    result = await encode_access_token(data)
    return result['token']
