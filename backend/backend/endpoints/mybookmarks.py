
from typing import Final
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status, HTTPException
from backend.common import dependencies
from backend.common.dao.bookmarks import get_bookmark_metadata
from backend.common.security import constants
from backend.common.schema import AccessTokenData, MyBookmarkMeta

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
        "Requires at least 'my.bookmarks.administrator' role"
    ),
    dependencies=[Depends(check_view_access)],
    response_model=MyBookmarkMeta
)
def get_metadata(
    token_data: AccessTokenData = Depends(dependencies.get_token_data),
    db: Session = Depends(dependencies.get_db)
):
    result = get_bookmark_metadata(db, token_data.user_id)

    # handle database error
    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.message
        )

    return result.data
