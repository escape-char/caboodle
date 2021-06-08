from typing import Final
from fastapi import Depends, APIRouter
from backend.common import dependencies
from backend.common.security import constants
from backend.common.schema import User

RESOURCE: Final[str] = constants.Resource.MY_PROFILE

router = APIRouter(prefix="/my/profile", tags=['profile'])


@router.get('/',  response_model=User)
def get_profile(
    session=Depends(dependencies.get_user_session),
    dependencies=[
        dependencies.CheckAccess(
            resource=RESOURCE,
            roles=[
                constants.Role.MY_PROFILE_VIEWER,
                constants.Role.MY_PROFILE_EDITOR
            ]
        )
    ]
):
    return session


@router.patch('/', response_model=User)
def update_profile(
    session=Depends(dependencies.get_user_session),
    db=Depends(dependencies.get_db),
    cache=Depends(dependencies.get_cache),
    dependencies=[
        dependencies.CheckAccess(
            resource=RESOURCE,
            roles=[
                constants.Role.MY_PROFILE_VIEWER,
                constants.Role.MY_PROFILE_EDITOR
            ]
        )
    ]
):
    pass
