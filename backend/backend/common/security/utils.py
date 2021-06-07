from typing import Final, List
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from backend.common.schema import AccessTokenData, User
from backend.settings import settings
from backend.common.utils import min_from_now
from backend.common.security import constants

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
ERROR_INVALID_RESOURCE: Final[str] = "invalid resource provided"
ERROR_INVALID_ROLE: Final[str] = "invalid role provided"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def gen_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def encode_access_token(
    data: AccessTokenData,
    secret_key: str = settings.auth_secret_key,
    expires_delta: timedelta = None,
    algorithm=settings.auth_algorithm
) -> dict:

    encode: dict = data.copy().dict()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = min_from_now(settings.auth_expire)

    encode.update({"exp": expire})

    token: Final[str] = jwt.encode(encode, secret_key, algorithm=algorithm)

    return dict(
        token=token,
        expires_at=str(expire)
    )


async def decode_access_token(
    access_token: str,
    secret_key: str = settings.auth_secret_key,
    algorithm: str = settings.auth_algorithm
) -> AccessTokenData:
    token_data: dict = jwt.decode(
        access_token,
        secret_key,
        algorithms=[algorithm]
    )
    return AccessTokenData(**token_data)


def has_access(
    session: User,
    resource: str,
    roles: List[str]
) -> bool:
    all_roles: List[str] = list(constants.Role.asdict().values())

    if resource not in list(constants.Resource.asdict().values()):
        raise ValueError(ERROR_INVALID_RESOURCE)

    resource_roles: List[str] = [
        r for r in all_roles if r.startswith(resource)
    ]
    user_roles: List[str] = [
        r.name for r in session.roles if r.name.startswith(resource)
    ]

    if not set(roles).issubset(set(resource_roles)):
        raise ValueError(ERROR_INVALID_ROLE)

    return bool(set(roles).intersection(user_roles))
