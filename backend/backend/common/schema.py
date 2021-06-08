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
    iss: str
