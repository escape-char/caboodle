from typing import Final, Optional
from fastapi import Request
from jose import JWTError
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.common.dependencies import get_db, get_cache
from backend.common.dao import users
from backend.common.security.utils import encode_access_token
from backend.common.schema import User, AccessTokenData, DatabaseResult
from backend.common.models import User as DBUser
from backend.settings import settings
from backend.common.session import set_session, get_ip

router = APIRouter()


MSG_UNAUTHENTICATED: Final[str] = "Invalid username or password"
MSG_ENCODE_TOKEN: Final[str] = "Failed to generate access token"
MSG_LOCKED: Final[str] = "Your account is locked. Please try again in an hour"


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_at: str
    user: User


@router.post('/auth', tags=['auth'], response_model=AuthResponse)
async def auth(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    cache: Session = Depends(get_cache)
):
    result: DatabaseResult = users.verify_auth(
        db,
        form.username,
        form.password
    )
    user: Optional[DBUser] = result.data

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MSG_UNAUTHENTICATED
        )

    if not result.success:
        # database exception
        if result.exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.message
            )
        else:
            # handle if user is locked
            if user.is_locked():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=MSG_LOCKED
                )
            else:
                # keep track of invalid login attempts
                # and lock them out if max retries
                result = users.set_invalid_login(db, user.id)

                # handle database error
                if not result.success:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=result.message
                    )
                # handle invalid login error
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=MSG_UNAUTHENTICATED
                    )

    result = users.set_successful_login(db, user.id)

    # handle database error
    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.message
        )

    # generate access token
    token_data = AccessTokenData(
        sub=user.id,
        user_id=user.id,
        name=user.name,
        email=user.email,
        given_username=user.username,
        iss=settings.auth_iss
    )

    try:
        token_result: dict = await encode_access_token(token_data)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MSG_ENCODE_TOKEN
        )

    await set_session(
        cache,
        User(**user.asdict()),
        token_result["token"],
        get_ip(request)
    )

    return AuthResponse(
        access_token=token_result["token"],
        token_type="bearer",
        expires_at=token_result["expires_at"],
        user=user
    )
