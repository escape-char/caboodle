from typing import Final, Optional
from jose import JWTError
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.common.dependencies import get_db
from backend.common.dao import users
from backend.common.security.utils import encode_access_token
from backend.common.schema import User, AccessTokenData, DatabaseResult
from backend.common.models import User as DBUser
from backend.settings import settings

router = APIRouter()


MSG_UNAUTHENTICATED: Final[str] = "Invalid username or password"
MSG_ENCODE_TOKEN: Final[str] = "Failed to generate access token"
MSG_LOCKED: Final[str] = "Your account is locked. Please try again in an hour"


class AuthResponse(BaseModel):
    token: str
    expires_at: str
    user: User


@router.post('/auth', tags=['auth'], response_model=AuthResponse)
async def auth(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
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
                    return HTTPException(
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
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.message
        )

    # generate access token
    token_data = AccessTokenData(
        sub=user.username,
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

    return AuthResponse(
        token=token_result["token"],
        expires_at=token_result["expires_at"],
        user=user
    )
