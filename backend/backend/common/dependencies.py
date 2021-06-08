from typing import Final, List
from jose.jwt import JWTError
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from backend.common.database import SessionLocal
from backend.common.cache import get_cache as get_cache_db, Cache
from backend.common.session import get_session, get_ip
from backend.common.security.utils import decode_access_token, has_access
from backend.common.schema import AccessTokenData, User


auth_exc: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="you are not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)

access_exc: HTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have access to this resource"
)

oauth2_scheme: Final[OAuth2PasswordBearer] = OAuth2PasswordBearer(
    tokenUrl="auth"
)


async def return_value(value):
    return value


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_cache() -> Cache:
    return await get_cache_db()


async def get_token_data(token: str = Depends(oauth2_scheme)):
    try:
        payload: Final[AccessTokenData] = await decode_access_token(token)

        if not payload.sub:
            raise auth_exc

        return payload
    except JWTError:
        raise auth_exc


async def get_user_session(
    request: Request,
    token: str = Depends(oauth2_scheme),
    token_data: AccessTokenData = Depends(get_token_data),
    cache=Depends(get_cache),
) -> User:
    return await get_session(cache, token, get_ip(request))


class CheckAccess:
    def __init__(
        self,
        session: User = Depends(get_user_session),
        resource: str = "",
        roles: List[str] = []
    ):
        self.session = session
        self.resource = resource
        self.roles = roles

    def __call__(self):
        if not has_access(self.session, self.resource, self.roles):
            raise access_exc
        else:
            return True
