
from typing import Final, Dict, List
from backend.common.utils import (cls_as_dict, cls_as_tuple)


class Resource:
    BOOKMARKS: Final[str] = "bookmarks"
    MY_BOOKMARKS: Final[str] = "my.bookmarks"
    MY_PROFILE: Final[str] = "my.profile"
    USERS: Final[str] = "users"

    @staticmethod
    def asdict():
        return cls_as_dict(Resource)

    @staticmethod
    def astuple():
        return cls_as_tuple(Resource)


resource_descr: Final[Dict[str, str]] = {
    Resource.BOOKMARKS:  "resource for managing all bookmarks",
    Resource.MY_BOOKMARKS:  "resource for managing user's bookmarks",
    Resource.MY_PROFILE: "resource for managing user's profile",
    Resource.USERS: "resource for managing all users"
}


class Permission:
    CREATE: Final[str] = "create"
    DELETE: Final[str] = "delete"
    EDIT: Final[str] = "edit"
    VIEW: Final[str] = "view"

    @staticmethod
    def asdict():
        return cls_as_dict(Permission)

    @staticmethod
    def astuple():
        return cls_as_tuple(Permission)


class ResourcePermission:
    BOOKMARKS_VIEW: Final[str] = f"{Resource.BOOKMARKS}.{Permission.VIEW}"
    BOOKMARKS_EDIT: Final[str] = f"{Resource.BOOKMARKS}.{Permission.EDIT}"
    BOOKMARKS_DELETE: Final[str] = f"{Resource.BOOKMARKS}.{Permission.DELETE}"

    MY_BOOKMARKS_VIEW: Final[str] = (
        f"{Resource.MY_BOOKMARKS}.{Permission.VIEW}"
    )
    MY_BOOKMARKS_EDIT: Final[str] = (
        f"{Resource.MY_BOOKMARKS}.{Permission.EDIT}"
    )
    MY_BOOKMARKS_CREATE: Final[str] = (
        f"{Resource.MY_BOOKMARKS}.{Permission.CREATE}"
    )
    MY_BOOKMARKS_DELETE: Final[str] = (
        f"{Resource.MY_BOOKMARKS}.{Permission.DELETE}"
    )

    MY_PROFILE_VIEW: Final[str] = f"{Resource.MY_PROFILE}.{Permission.VIEW}"
    MY_PROFILE_EDIT: Final[str] = f"{Resource.MY_PROFILE}.{Permission.EDIT}"

    USERS_VIEW: Final[str] = f"{Resource.USERS}.{Permission.VIEW}"
    USERS_EDIT: Final[str] = f"{Resource.USERS}.{Permission.EDIT}"
    USERS_CREATE: Final[str] = f"{Resource.USERS}.{Permission.CREATE}"
    USERS_DELETE: Final[str] = f"{Resource.USERS}.{Permission.DELETE}"

    @staticmethod
    def asdict():
        return cls_as_dict(ResourcePermission)

    @staticmethod
    def astuple():
        return cls_as_tuple(ResourcePermission)


permission_descr: Final[Dict[str, str]] = {
    # bookmark permissions
    ResourcePermission.BOOKMARKS_VIEW: "user can view all bookmarks",
    ResourcePermission.BOOKMARKS_EDIT: "user can edit any bookmarks",
    ResourcePermission.BOOKMARKS_DELETE: "user can delete any bookmarks",

    # user's bookmark permissions
    ResourcePermission.MY_BOOKMARKS_VIEW: (
        "user can view their own bookmarks"
    ),
    ResourcePermission.MY_BOOKMARKS_EDIT: (
        "user can edit their own bookmarks"
    ),
    ResourcePermission.MY_BOOKMARKS_CREATE: (
        "user can create their own bookmarks"
    ),
    ResourcePermission.MY_BOOKMARKS_DELETE: (
        "user can view delete own bookmarks"
    ),

    # user's bookmark permissions
    ResourcePermission.MY_PROFILE_VIEW: (
        "user can view their own profile"
    ),
    ResourcePermission.MY_PROFILE_EDIT: (
        "user can edit their own profile"
    ),

    # users permission
    ResourcePermission.USERS_VIEW: "user can view all users",
    ResourcePermission.USERS_EDIT: "user can edit a user",
    ResourcePermission.USERS_CREATE: "user can create a user",
    ResourcePermission.USERS_DELETE: "user can delete a user"
}


class Role:
    BOOKMARKS_VIEWER: Final[str] = f"{Resource.BOOKMARKS}.viewer"
    BOOKMARKS_EDITOR: Final[str] = f"{Resource.BOOKMARKS}.editor"
    BOOKMARKS_ADMINISTRATOR: Final[str] = f"{Resource.BOOKMARKS}.administrator"

    MY_BOOKMARKS_VIEWER: Final[str] = f"{Resource.MY_BOOKMARKS}.viewer"
    MY_BOOKMARKS_EDITOR: Final[str] = f"{Resource.MY_BOOKMARKS}.editor"
    MY_BOOKMARKS_ADMINISTRATOR: Final[str] = (
        f"{Resource.MY_BOOKMARKS}.administrator"
    )

    MY_PROFILE_VIEWER: Final[str] = f"{Resource.MY_PROFILE}.viewer"
    MY_PROFILE_EDITOR: Final[str] = f"{Resource.MY_PROFILE}.editor"

    USERS_VIEWER: Final[str] = f"{Resource.USERS}.viewer"
    USERS_EDITOR: Final[str] = f"{Resource.USERS}.editor"
    USERS_ADMINISTRATOR: Final[str] = f"{Resource.USERS}.administrator"

    @staticmethod
    def asdict():
        return cls_as_dict(Role)

    @staticmethod
    def astuple():
        return cls_as_tuple(Role)


role_descr: Final[Dict[str, str]] = {
    Role.BOOKMARKS_VIEWER: "user can view all bookmarks",
    Role.BOOKMARKS_EDITOR: "user can edit all bookmarks",
    Role.BOOKMARKS_ADMINISTRATOR: "User can create and delete bookmarks",

    Role.MY_BOOKMARKS_VIEWER: "user can view their own bookmarks",
    Role.MY_BOOKMARKS_EDITOR: "user can edit their own bookmarks",
    Role.MY_BOOKMARKS_ADMINISTRATOR: "user can manage their own bookmarks",

    Role.MY_PROFILE_VIEWER: "user can view their own profile",
    Role.MY_PROFILE_EDITOR: "user can edit their own profile",

    Role.USERS_VIEWER: "user can view all users",
    Role.USERS_EDITOR: "user can edit all users",
    Role.USERS_ADMINISTRATOR: "User can manage all users"
}

role_to_perms: Dict[str, List[str]] = {
    # Bookmarks
    Role.BOOKMARKS_VIEWER: [ResourcePermission.BOOKMARKS_VIEW],
    Role.BOOKMARKS_EDITOR: [
        ResourcePermission.BOOKMARKS_VIEW,
        ResourcePermission.MY_BOOKMARKS_EDIT
    ],
    Role.BOOKMARKS_ADMINISTRATOR: [
        ResourcePermission.BOOKMARKS_VIEW,
        ResourcePermission.BOOKMARKS_EDIT,
        ResourcePermission.BOOKMARKS_DELETE
    ],

    # my bookmarks
    Role.MY_BOOKMARKS_VIEWER: [ResourcePermission.MY_BOOKMARKS_VIEW],
    Role.MY_BOOKMARKS_EDITOR: [
        ResourcePermission.MY_BOOKMARKS_VIEW,
        ResourcePermission.MY_BOOKMARKS_EDIT
    ],
    Role.MY_BOOKMARKS_ADMINISTRATOR: [
        ResourcePermission.MY_BOOKMARKS_VIEW,
        ResourcePermission.MY_BOOKMARKS_EDIT,
        ResourcePermission.MY_BOOKMARKS_CREATE,
        ResourcePermission.MY_BOOKMARKS_DELETE
    ],

    # users
    Role.USERS_VIEWER: [ResourcePermission.USERS_VIEW],
    Role.USERS_EDITOR: [
        ResourcePermission.USERS_VIEW,
        ResourcePermission.USERS_EDIT
    ],
    Role.USERS_ADMINISTRATOR: [
        ResourcePermission.USERS_VIEW,
        ResourcePermission.USERS_EDIT,
        ResourcePermission.USERS_CREATE,
        ResourcePermission.USERS_DELETE
    ],

    # profile
    Role.MY_PROFILE_VIEWER: [ResourcePermission.MY_PROFILE_VIEW],
    Role.MY_PROFILE_EDITOR: [
        ResourcePermission.MY_PROFILE_VIEW,
        ResourcePermission.MY_PROFILE_EDIT
    ],
}

default_user_roles: Final[List[str]] = [
    Role.BOOKMARKS_ADMINISTRATOR,
    Role.MY_BOOKMARKS_ADMINISTRATOR,
    Role.MY_PROFILE_EDITOR,
    Role.USERS_ADMINISTRATOR
]
