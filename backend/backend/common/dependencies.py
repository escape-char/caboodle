from typing import Final, List, Optional
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


async def get_token_data(
    token: str = Depends(oauth2_scheme)
) -> AccessTokenData:
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
    cache=Depends(get_cache),
    token_data=Depends(get_token_data),
) -> User:
    session: Optional[User] = await get_session(cache, token, get_ip(request))
    if not session:
        raise auth_exc
    return session


class CheckAccess:
    def __init__(
        self,
        resource: str = "",
        roles: List[str] = []
    ):
        self.resource = resource
        self.roles = roles

    def __call__(self, session=Depends(get_user_session)):
        if not has_access(session, self.resource, self.roles):
            raise access_exc
        else:
            return True


def check_access_factory(
    session: User = Depends(get_user_session),
    resource: str = "",
    roles: List[str] = []
) -> CheckAccess:
    raise NameError(str(session))
    return CheckAccess(session, resource, roles)
