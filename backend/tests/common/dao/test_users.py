import pytest
from sqlalchemy import or_
from typing import List, Final
from unittest.mock import MagicMock
from backend.common.models import User
from backend.common.schema import (
    DatabaseResult,
    UserCreate as UserCreateSchema,
    UserUpdate as UserUpdateSchema
)
from backend.common.dao import users

USER_ID: Final[int] = 22


@pytest.fixture
def dao_users() -> List[User]:
    return [
        User(
            id=22,
            username="testuser",
            name="test test",
            email="test@testing.not"
        )
    ]


@pytest.fixture
def dao_user() -> User:
    return User(
        id=22,
        username="testuser",
        name="test test",
        email="test@testing.not"
    )


@pytest.fixture
def create_user() -> UserCreateSchema:
    return UserCreateSchema(
        username="testuser",
        name="test test",
        email="test@testing.not",
        password="testpass"
    )


@pytest.fixture
def update_user() -> UserUpdateSchema:
    return UserUpdateSchema(
        username="testuser2",
        name="test test2",
        email="test@testing.not2",
        password="testpass"
    )


def test_get_users(dao_users):

    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value.offset.return_value.\
        limit.return_value.all.return_value = dao_users
    result: DatabaseResult = users.get_users(mock_db)

    mock_db.query.assert_called_once_with(User)
    mock_db.query().offset.assert_called_once_with(0)
    mock_db.query().offset().limit.assert_called_once_with(50)

    assert result.data[0] == dao_users[0]


def test_get_users_search(dao_users):
    search: Final[str] = "test"
    sql_search: Final[str] = f"%{search}%".lower()
    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value.filter.return_value.offset.return_value.\
        limit.return_value.all.return_value = dao_users

    # need to verify or condition for search is called
    result: DatabaseResult = users.get_users(mock_db, search="test")

    mock_db.query.assert_called_once_with(User)
    assert mock_db.query().filter[0][0].compare(
        or_(
            User.username.like(sql_search),
            User.email.like(sql_search),
            User.name.like(sql_search)
        )
    )
    mock_db.query().filter().offset.assert_called_once_with(0)
    mock_db.query().filter().offset().limit.assert_called_once_with(50)

    assert result.data[0] == dao_users[0]


def test_get_by_username(dao_user):
    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value.filter.return_value.\
        first.return_value = dao_user

    result: DatabaseResult = users.get_user_by_username(
        mock_db, dao_user.username
    )

    mock_db.query.assert_called_once_with(User)

    assert mock_db.query().filter.call_args[0][0].compare(
        User.username == dao_user.username.lower()
    )
    mock_db.query().filter().first.assert_called()
    assert result.data == dao_user


def test_get_by_id(dao_user):
    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value.filter.return_value.\
        first.return_value = dao_user

    result: DatabaseResult = users.get_user_by_id(
        mock_db, dao_user.id
    )

    mock_db.query.assert_called_once_with(User)
    assert mock_db.query().filter.call_args[0][0].compare(
        User.id == dao_user.id
    )
    mock_db.query().filter().first.assert_called()
    assert result.data == dao_user


def test_create_user(create_user):

    def refresh(u: User):
        u.id = USER_ID

    mock_db: MagicMock = MagicMock()
    mock_db.refresh = refresh

    result: DatabaseResult = users.create_user(mock_db, create_user)

    #  make sure password is hashed when in db
    assert mock_db.add.call_args[0][0].password != create_user.password
    mock_db.commit.assert_called()

    # check returns user id and info
    assert (
        result.data.id == USER_ID and
        result.data.username == create_user.username and
        result.data.name == create_user.name and
        result.data.email == create_user.email
    )


def test_update_user(update_user, dao_user):
    mock_db: MagicMock = MagicMock()

    mock_db.query.return_value.filter.return_value.\
        one.return_value = dao_user

    result: DatabaseResult = users.update_user(
        mock_db,
        USER_ID,
        update_user
    )

    assert mock_db.query().filter.call_args[0][0].compare(
        User.id == USER_ID
    )

    mock_db.query().filter().one.assert_called()

    mock_db.commit.assert_called()

    assert (
        result.data.id == USER_ID and
        result.data.username == update_user.username and
        result.data.name == update_user.name and
        result.data.email == update_user.email
    )


def test_lock_user(dao_user):
    mock_db: MagicMock = MagicMock()

    mock_db.query.return_value.filter.return_value.\
        one.return_value = dao_user

    result: DatabaseResult = users.lock_user(mock_db, USER_ID)

    assert mock_db.query().filter.call_args[0][0].compare(
        User.id == USER_ID
    )

    mock_db.query().filter().one.assert_called()
    mock_db.commit.assert_called()
    assert result.data.is_locked()


def test_unlock_user(dao_user: User):
    user2: Final[User] = User(**dao_user.asdict())
    user2.lock_account()

    mock_db: MagicMock = MagicMock()

    mock_db.query.return_value.filter.return_value.\
        one.return_value = user2

    result: DatabaseResult = users.unlock_user(mock_db, USER_ID)

    assert mock_db.query().filter.call_args[0][0].compare(
        User.id == USER_ID
    )
    mock_db.query().filter().one.assert_called()
    mock_db.commit.assert_called()

    assert result.data and not result.data.is_locked()


def test_set_successful_login(dao_user: User):
    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value.filter.return_value.\
        one.return_value = dao_user

    result: DatabaseResult = users.set_successful_login(mock_db, USER_ID)

    assert mock_db.query().filter.call_args[0][0].compare(
        User.id == USER_ID
    )
    mock_db.query().filter().one.assert_called()
    mock_db.commit.assert_called()

    assert result.data and bool(result.data.last_login)


def test_set_invalid_login_locked(dao_user: User):
    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value.filter.return_value.\
        one.return_value = dao_user

    users.set_invalid_login(mock_db, USER_ID)
    users.set_invalid_login(mock_db, USER_ID)

    result: DatabaseResult = users.set_invalid_login(mock_db, USER_ID)

    assert mock_db.query().filter.call_args[0][0].compare(
        User.id == USER_ID
    )

    assert mock_db.commit.call_count == 3
    assert result.data and result.data.is_locked()


def test_delete_user(dao_user):
    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value.filter.return_value.\
        one.return_value = dao_user

    result: DatabaseResult = users.delete_user(mock_db, USER_ID)

    assert mock_db.query().filter.call_args[0][0].compare(
        User.id == USER_ID
    )
    mock_db.query().filter().one.assert_called()

    assert mock_db.delete.call_args[0][0].id == dao_user.id
    assert result.data and result.data.id == dao_user.id


def test_verify_auth_no_user(dao_user):
    password: Final[str] = "testpassword"
    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value.filter.return_value.\
        first.return_value = None

    result: DatabaseResult = users.verify_auth(
        mock_db,
        dao_user.username,
        password
    )

    assert mock_db.query().filter.call_args[0][0].compare(
        User.username == dao_user.username
    )
    mock_db.query().filter().first.assert_called()

    assert not result.success and not result.data


def test_verify_auth_success(dao_user):
    user2: Final[User] = User(**dao_user.asdict())

    password: Final[str] = "testpassword"
    mock_db: MagicMock = MagicMock()

    user2.set_password(password)

    mock_db.query.return_value.filter.return_value.\
        first.return_value = user2

    result: DatabaseResult = users.verify_auth(
        mock_db,
        user2.username,
        password
    )

    assert mock_db.query().filter.call_args[0][0].compare(
        User.username == user2.username
    )
    mock_db.query().filter().first.assert_called()
    assert result.success and result.data and result.data.id == dao_user.id


def test_verify_auth_invalid(dao_user):
    password: Final[str] = "testpassword"
    invalid_password: Final[str] = "invalidpassword"

    user2: Final[User] = User(**dao_user.asdict())

    user2.set_password(password)

    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value.filter.return_value.\
        first.return_value = None

    result: DatabaseResult = users.verify_auth(
        mock_db,
        user2.username,
        invalid_password
    )

    assert mock_db.query().filter.call_args[0][0].compare(
        User.username == user2.username
    )
    mock_db.query().filter().first.assert_called()
    assert not result.success and not result.data
