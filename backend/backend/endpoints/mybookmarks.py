from typing import Final, List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status, HTTPException
from backend.common import dependencies
from backend.common.dao import mybookmarks
from backend.common.security import constants
from backend.common.schema import (
    AccessTokenData,
    DatabaseResult,
    MyBookmarkMeta,
    MyBookmarksParams,
    Bookmark
)

RESOURCE: Final[str] = constants.Resource.MY_BOOKMARKS


router = APIRouter(
    prefix="/my/bookmarks",
    tags=['my bookmarks']
)


check_view_access = dependencies.CheckAccess(
    RESOURCE,
    [
        constants.Role.MY_BOOKMARKS_ADMINISTRATOR,
        constants.Role.MY_BOOKMARKS_EDITOR,
        constants.Role.MY_BOOKMARKS_VIEWER,
    ]
)

check_edit_access = dependencies.CheckAccess(
    RESOURCE,
    [
        constants.Role.MY_BOOKMARKS_ADMINISTRATOR,
        constants.Role.MY_BOOKMARKS_EDITOR
    ]
)
check_delete_access = dependencies.CheckAccess(
    RESOURCE,
    [
        constants.Role.MY_BOOKMARKS_ADMINISTRATOR
    ]
)


@router.get(
    '/metadata',
    description=(
        "Gets user's bookmarks metadata including total favorites,"
        " bookmarks, unread, and unsorted."
        "Requires at least 'my.bookmarks.view' role"
    ),
    dependencies=[Depends(check_view_access)],
    response_model=MyBookmarkMeta
)
def get_metadata(
    token_data: AccessTokenData = Depends(dependencies.get_token_data),
    db: Session = Depends(dependencies.get_db)
):
    result: DatabaseResult = mybookmarks.get_bookmark_metadata(
        db,
        token_data.user_id
    )

    # handle database error
    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.message
        )

    return result.data


@router.get(
    '',
    description=(
        "Gets user's bookmarks. "
        "Requires at least 'my.bookmarks.view' role"
    ),
    dependencies=[Depends(check_view_access)],
    response_model=List[Bookmark]
)
def get_my_bookmarks(
    params: MyBookmarksParams = Depends(),
    token_data: AccessTokenData = Depends(dependencies.get_token_data),
    db: Session = Depends(dependencies.get_db)
):
    result: DatabaseResult = mybookmarks.get_my_bookmarks(
        db,
        token_data.user_id,
        params
    )

    # handle database error
    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.message
        )

    return result.data


@router.get(
    '/{bookmark_id}',
    description=(
        "Gets user's bookmark by id. "
        "Requires at least 'my.bookmarks.view' role"
    ),
    dependencies=[Depends(check_view_access)],
    response_model=Bookmark
)
def get_my_bookmark(
    bookmark_id: int,
    token_data: AccessTokenData = Depends(dependencies.get_token_data),
    db: Session = Depends(dependencies.get_db)
):
    result: DatabaseResult = mybookmarks.get_my_bookmark(
        db,
        bookmark_id,
        token_data.user_id
    )

    # handle database error
    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.message
        )
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    return result.data


