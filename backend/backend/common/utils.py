from datetime import datetime, timedelta
from functools import reduce
from urllib.parse import quote
from typing import Any, Dict, Union
from backend.settings import settings
from backend.common.constants import (ENV_DEVELOPMENT, ENV_PRODUCTION)


def get_conn_str(
    prot: str,
    host: str,
    port: int,
    username: str = None,
    password: str = None,
    db: Union[str, int] = None
) -> str:
    conn_str = ""

    if username and password:
        conn_str = "{pt}://{u}:{ps}@{h}:{po}".format(
            pt=prot,
            u=quote(username),
            ps=quote(password),
            h=host,
            po=port
        )
    else:
        conn_str = f"{prot}://{host}:{port}"

    if db:
        conn_str = f"{conn_str}/{db}"

    return conn_str


def cls_as_dict(cl) -> dict:
    v: dict = dict(vars(cl))
    return {
        k: v for k, v in v.items() if (
            not k.startswith("__") and not is_func(getattr(cl, k))
        )
    }


def cls_as_tuple(cl):
    d = cls_as_dict(cl)
    return [(k, v) for k, v in d.items()]


def is_func(f) -> bool:
    return callable(f)


def create_lookup(lis: list, key='name', value_key=None) -> Dict[str, Any]:
    def reduce_lookup(acc, v):
        acc[v[key]] = v if not value_key else v[value_key]
        return acc

    return reduce(reduce_lookup, lis, {})


def utcnow():
    return datetime.utcnow()


def map_timestamp(lt: list) -> list:
    def map_ts(v):
        now = utcnow()
        return {**v, "modified_at": now, "created_at": now}
    return [map_ts(v) for v in lt]


def min_from_now(minutes: int) -> datetime:
    return datetime.utcnow() + timedelta(minutes=minutes)


def has_expired(date: datetime) -> bool:
    return datetime.now() < date


def is_development():
    return settings.environment == ENV_DEVELOPMENT


def is_production():
    return settings.environment == ENV_PRODUCTION
