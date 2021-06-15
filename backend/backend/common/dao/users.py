from typing import List, Final, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, exc
from backend.common import schema
from backend.common import models
from backend.common.constants import ERROR_DATABASE


def get_users(
    db: Session,
    offset: Optional[int] = 0,
    limit: Optional[int] = 50,
    search: Optional[str] = ""
) -> schema.DatabaseResult:
    s: Final[str] = f"%{search}%".lower()

    try:
        query = db.query(models.User)
        if search:
            query.filter(
                or_(
                    models.User.username.like(s),
                    models.User.email.like(s),
                    models.User.name.like(s)
                )
            )
        users: List[models.User] = query.offset(offset).limit(limit).all()
        return schema.DatabaseResult(
            success=True,
            data=users
        )
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )


def get_user_by_id(db: Session, user_id: int) -> schema.DatabaseResult:
    try:
        user: models.User = db.query(models.User).filter(
            models.User.id == user_id
        ).first()
        return schema.DatabaseResult(success=True, data=user)
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )


def get_user_by_username(db: Session, username: str) -> schema.DatabaseResult:
    try:
        user: Optional[models.User] = db.query(models.User).filter(
            models.User.username == username.lower()
        ).first()
        return schema.DatabaseResult(success=True, data=user)
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )


def create_user(db: Session, user: schema.UserCreate) -> schema.DatabaseResult:
    db_user: models.User = models.User(
        username=user.username,
        email=user.email,
        name=user.name,
        dark_theme=user.dark_theme
    )
    db_user.set_password(user.password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return schema.DatabaseResult(success=True, data=db_user)
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )


def update_user(
    db: Session,
    user_id: int,
    user: schema.UserUpdate
) -> schema.DatabaseResult:

    db_user: models.User = db.query(models.User).filter(
        models.User.id == user_id
    ).one()

    for k, v in user.dict().items():
        setattr(db_user, k, v)

    try:
        db.commit()
        return schema.DatabaseResult(
            success=True,
            data=db_user
        )
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )


def lock_user(
    db: Session,
    user_id: int
) -> schema.DatabaseResult:

    db_user: models.User = db.query(models.User).filter(
        models.User.id == user_id
    ).one()

    db_user.lock_account()

    try:
        db.commit()
        return schema.DatabaseResult(success=True, data=db_user)
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )


def unlock_user(db: Session, user_id: int) -> schema.DatabaseResult:
    db_user: models.User = db.query(models.User).filter(
        models.User.id == user_id
    ).one()

    db_user.unlock_account()

    try:
        db.commit()
        return schema.DatabaseResult(success=True, data=db_user)
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )


def set_invalid_login(db: Session, user_id: int) -> schema.DatabaseResult:
    db_user: models.User = db.query(models.User).filter(
        models.User.id == user_id
    ).one()

    db_user.retries = min((db_user.retries or 0) + 1, 3)

    if db_user.has_max_retries:
        db_user.lock_account()

    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )

    return schema.DatabaseResult(success=True, data=db_user)


def set_successful_login(db: Session, user_id: int) -> schema.DatabaseResult:
    db_user: models.User = db.query(models.User).filter(
        models.User.id == user_id
    ).one()

    # clear any lock and retry state
    db_user.unlock_account()

    # update the user's last login timestamp
    db_user.set_last_login()
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )

    return schema.DatabaseResult(success=True, data=db_user)


def delete_user(db: Session, user_id: int) -> schema.DatabaseResult:
    db_user: Final[models.User] = db.query(models.User).filter(
        models.User.id == user_id
    ).one()

    try:
        db.delete(db_user)
        db.commit()
    except exc.SQLAlchemyError as e:
        return schema.DatabaseResult(
            success=False,
            exception=e,
            message=ERROR_DATABASE
        )

    return schema.DatabaseResult(success=True, data=db_user)


def verify_auth(
    db: Session,
    username: str,
    password: str
) -> schema.DatabaseResult:
    result: schema.DatabaseResult = get_user_by_username(db, username)

    if not result.success:
        return result

    user = result.data

    if not user:
        return schema.DatabaseResult(success=False)
    elif not user.verify_password(password):
        return schema.DatabaseResult(success=False, data=user)
    else:
        return schema.DatabaseResult(success=True, data=user)
