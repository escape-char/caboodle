from fastapi.testclient import TestClient
from fastapi import status
from typing import Final
from unittest.mock import patch
from backend.common.models import User as DBUser
from backend.common.schema import DatabaseResult
from tests.conftest import MOCK_DB_NAME


def get_db_user(locked=False) -> DBUser:
    user: DBUser = DBUser(
        id=2,
        username="testuser",
        name="test user",
        email="test@test.not",
    )
    if locked:
        user.lock_account()
    return user


@patch('backend.endpoints.auth.users')
class TestAuth:
    def test_auth_success(
        self,
        mock_users,
        web_app_client: TestClient
    ):

        user: Final[DBUser] = get_db_user()

        mock_users.verify_auth.return_value = DatabaseResult(
            success=True,
            data=user
        )
        mock_users.set_successful_login.return_value = DatabaseResult(
            success=True
        )

        username: Final[str] = user.username
        password: Final[str] = "testpassord"

        response = web_app_client.post(
            "/auth",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"username": username, "password": password}
        )
        json = response.json()

        assert mock_users.\
            verify_auth.call_args[0][0].\
            _extract_mock_name() == MOCK_DB_NAME

        assert mock_users.verify_auth.call_args[0][1] == username
        assert mock_users.verify_auth.call_args[0][2] == password

        assert mock_users.set_invalid_invalid_login.call_count == 0

        assert response.status_code == status.HTTP_200_OK
        assert "token" in json
        assert "expires_at" in json
        assert "user" in json and json["user"]["id"] == user.id

    def test_auth_invalid(
        self,
        mock_users,
        web_app_client: TestClient
    ):

        user: Final[DBUser] = get_db_user()

        mock_users.verify_auth.return_value = DatabaseResult(
            success=False,
            data=user
        )
        mock_users.set_invalid_login.return_value = DatabaseResult(
            success=True
        )

        username: Final[str] = user.username
        password: Final[str] = "testpassord"

        response = web_app_client.post(
            "/auth",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"username": username, "password": password}
        )
        json = response.json()

        assert mock_users.set_invalid_login.call_count == 1

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "token" not in json
        assert "expires_at" not in json
        assert "user" not in json
