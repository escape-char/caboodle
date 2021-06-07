from typing import Final, List, Dict, Tuple, Any
from functools import reduce
from backend.common.security.constants import (
    Resource,
    Role,
    ResourcePermission,
    resource_descr,
    role_descr,
    permission_descr,
    role_to_perms,
    default_user_roles
)
from backend.common.utils import create_lookup


def get_resources() -> List[Dict[str, str]]:
    resources: Final[Tuple] = Resource.astuple()

    return [
        {"name": r[1], "description": resource_descr[r[1]]} for r in resources
    ]


def _map_entity(v, id_lookup, descr_lookup):
    r = ".".join(v[1].split(".")[:-1])

    return dict(
        name=v[1],
        resource_id=id_lookup[r],
        description=descr_lookup[v[1]]
    )


def get_roles_from_resources(resources: List[dict]) -> List[dict]:
    role_tuple: Tuple[str, str] = Role.astuple()

    id_lookup: Dict[str, Any] = create_lookup(resources, 'name', 'id')

    return [_map_entity(r, id_lookup, role_descr) for r in role_tuple]


def get_perms_from_resources(resources: list) -> List[dict]:
    perm_tuple: Tuple[str, str] = ResourcePermission.astuple()

    id_lookup:  Dict[str, Any] = create_lookup(resources, 'name', 'id')

    return [_map_entity(p, id_lookup, permission_descr) for p in perm_tuple]


def get_role_perm(role_p: dict) -> List[dict]:
    def reduce_role_perm(acc, value):
        acc["permissions"] = [
            *acc.get("permissions", []),
            *value["permissions"]
        ]
        acc["roles"] = [
            *acc.get("roles", []),
            *value["roles"]
        ]
        return acc

    role_perm: Final[dict] = reduce(reduce_role_perm, role_p, {})

    perm_id_lookup = create_lookup(role_perm["permissions"], 'name', 'id')

    def reduce_role(acc: list, v: dict) -> List[dict]:
        perms: Final[List[dict]] = [
            {
               "role_id": v["id"],
               "permission_id": perm_id_lookup[p]
            }

            for p in role_to_perms[v["name"]]
        ]
        return [*acc, *perms]

    return reduce(reduce_role, role_perm["roles"], [])


def get_user_roles(user: dict, roles: list) -> List[dict]:
    role_id_lookup: Final[Dict[str, int]] = create_lookup(roles, "name", "id")

    return [
        {"user_id": user["id"], "role_id": role_id_lookup[r]}
        for r in default_user_roles
    ]
