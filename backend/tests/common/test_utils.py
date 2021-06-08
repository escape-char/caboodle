from unittest.mock import patch
from typing import Final, List, Dict
from datetime import datetime, timedelta
from urllib.parse import quote
from backend.common import utils
from backend.common.constants import ENV_DEVELOPMENT, ENV_PRODUCTION


def test_conn_str():
    protocol: Final[str] = "postgres"
    host: Final[str] = "localhost"
    username: Final[str] = "test_user"
    password: Final[str] = "password"
    port: Final[str] = 5432
    db: Final[str] = "testing"

    conn_str1: Final[str] = utils.get_conn_str(
        protocol,
        host,
        port,
        username,
        password,
        db
    )

    conn_str2: Final[str] = utils.get_conn_str(
        protocol,
        host,
        port,
        db=db
    )

    assert conn_str1 == "{pro}://{user}:{password}@{host}:{port}/{db}".format(
        pro=protocol,
        user=quote(username),
        password=quote(password),
        host=host,
        port=port,
        db=db
    )

    assert conn_str2 == "{pro}://{host}:{port}/{db}".format(
        pro=protocol,
        host=host,
        port=port,
        db=db
    )


def test_cls_as_dict():
    class TestClass:
        test1 = "test1value"
        test2 = "test2value"

    assert (
        utils.cls_as_dict(TestClass) == {
            "test1": TestClass.test1,
            "test2": TestClass.test2
        }
    )


def test_cls_as_tuple():
    class TestClass:
        test1 = "test1val"
        test2 = "test2val"

    assert (
        utils.cls_as_tuple(TestClass) == [
            ("test1", "test1val"), ("test2", "test2val")
        ]
    )


def test_create_lookup():
    t_list: List[Dict] = [
        {
            "name": "john.doe",
            "id": 20,
            "age": "100"
        },
        {
            "name": "jane.doe",
            "id": 5,
            "age": "101"
        },
        {
            "name": "will.doe",
            "id": 30,
            "age": "100"
        },
    ]

    lookup: dict = utils.create_lookup(t_list)

    assert(lookup["john.doe"] == t_list[0])
    assert(lookup["jane.doe"] == t_list[1])
    assert(lookup["will.doe"] == t_list[2])

    lookup = utils.create_lookup(t_list, key='id')

    assert lookup[20] == t_list[0]
    assert lookup[5] == t_list[1]
    assert lookup[30] == t_list[2]


def test_utcnow():
    now: Final[str] = str(datetime.utcnow()).split(".")[0]
    now2: Final[str] = str(utils.utcnow()).split(".")[0]

    assert now == now2


def test_map_timestamp():
    t_list: List[Dict] = [
        {
            "name": "test1"
        },
        {
            "name": "test2"
        }
    ]
    now: Final[str] = str(datetime.utcnow()).split(".")[0]
    ts: List[Dict] = utils.map_timestamp(t_list)

    for t in ts:
        assert str(t["modified_at"]).split(".")[0] == now
        assert str(t["created_at"]).split(".")[0] == now


def test_min_from_now():
    min: Final[int] = 15
    fu1: Final[str] = str(
        datetime.utcnow() + timedelta(minutes=min)
    ).split(".")[0]
    fu2: Final[str] = str(utils.min_from_now(min)).split(".")[0]

    assert fu1 == fu2


def has_expired():
    expired: Final[datetime] = datetime.utcnow() - timedelta(minutes=10)

    assert(utils.has_expired(expired))


def test_is_dev():
    with patch("backend.common.utils.settings") as mock_settings:
        mock_settings.environment = ENV_DEVELOPMENT
        assert not utils.is_production() and utils.is_development()


def test_is_prod():
    with patch("backend.common.utils.settings") as mock_settings:
        mock_settings.environment = ENV_PRODUCTION
        assert not utils.is_development() and utils.is_production()
