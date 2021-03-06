from enum import Enum
from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel


class DatabaseResult:

    def __init__(
        self,
        success: bool = True,
        data: Any = None,
        message: str = None,
        exception: Exception = None
    ):

        self.success = success
        self.data = data
        self.message = message
        self.exception = exception


class PermissionBase(BaseModel):
    name: str
    description: str
    resource_id: int
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    name: str
    description: str
    resource_id: int
    permissions: Optional[List[Permission]]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class ResourceBase(BaseModel):
    name: str
    description: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class ResourceCreate(ResourceBase):
    pass


class Resource(ResourceBase):
    id: int
    roles: Optional[List[Role]]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    name: str
    dark_theme: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str


class User(UserBase):
    id: int
    retries: Optional[int] = 0
    locked_until: Optional[datetime] = None
    last_login: Optional[datetime]
    roles: List[Role]

    created_at: Optional[datetime]
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True


class AccessTokenData(BaseModel):
    sub: str
    name: str
    email: str
    given_username: str
    user_id: int
    iss: str


class MyBookmarkMeta(BaseModel):
    bookmarks: int = 0
    favorites: int = 0
    unread: int = 0
    unsorted: int = 0


class CommonParams(BaseModel):
    q: Optional[str] = None
    skip: int = 0
    limit: int = 100


class MyBookmarkSortByEnum(Enum):
    create_date = "created_at"
    modified_date = "modified_at"
    title = "title"


class MyBookmarksParams(CommonParams):
    unsorted: Optional[bool] = None
    favorite: Optional[bool] = None
    unread: Optional[bool] = None
    sort_by: MyBookmarkSortByEnum = (
        MyBookmarkSortByEnum.modified_date
    )


class BookmarkBase(BaseModel):
    user_id: int
    title: str
    description: str
    image_path: Optional[str] = None
    snapshot_id: Optional[int] = None
    to_read: bool = False
    favorite: bool = False


class Bookmark(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    image_path: Optional[str] = None
    snapshot_id: Optional[int] = None
    to_read: bool = False
    favorite: bool = False

    created_at: Optional[datetime]
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True
