from enum import Enum


class Permission(str, Enum):
    USERS_VIEW = "users.view"
    USERS_EDIT = "users.edit"

    ROLES_VIEW = "roles.view"
    ROLES_EDIT = "roles.edit"

    RESTAURANTS_VIEW = "restaurants.view"
    RESTAURANTS_EDIT = "restaurants.edit"

    WAREHOUSE_VIEW = "warehouse.view"
    WAREHOUSE_EDIT = "warehouse.edit"

    FINANCE_VIEW = "finance.view"
    FINANCE_EDIT = "finance.edit"

    ANALYTICS_VIEW = "analytics.view"

    STAFF_VIEW = "staff.view"
    STAFF_EDIT = "staff.edit"

    SETTINGS_VIEW = "settings.view"
    SETTINGS_EDIT = "settings.edit"


ROLE_PERMISSIONS = {
    "director": {
        permission.value
        for permission in Permission
    },

    "manager": {
        Permission.RESTAURANTS_VIEW.value,
        Permission.RESTAURANTS_EDIT.value,

        Permission.WAREHOUSE_VIEW.value,
        Permission.WAREHOUSE_EDIT.value,

        Permission.ANALYTICS_VIEW.value,

        Permission.STAFF_VIEW.value,
    },

    "accountant": {
        Permission.FINANCE_VIEW.value,
        Permission.FINANCE_EDIT.value,

        Permission.ANALYTICS_VIEW.value,
    },

    "warehouse": {
        Permission.WAREHOUSE_VIEW.value,
        Permission.WAREHOUSE_EDIT.value,
    },

    "cashier": {
        Permission.RESTAURANTS_VIEW.value,
        Permission.WAREHOUSE_VIEW.value,
    },

    "hr": {
        Permission.USERS_VIEW.value,
        Permission.USERS_EDIT.value,

        Permission.STAFF_VIEW.value,
        Permission.STAFF_EDIT.value,
    },

    "it": {
        Permission.USERS_VIEW.value,

        Permission.RESTAURANTS_VIEW.value,

        Permission.SETTINGS_VIEW.value,
        Permission.SETTINGS_EDIT.value,
    },

    "user": {
        Permission.RESTAURANTS_VIEW.value,
    },
}


def has_permission(
    role: str,
    permission: Permission,
) -> bool:

    permissions = ROLE_PERMISSIONS.get(
        role,
        set(),
    )

    return permission.value in permissions


def get_role_permissions(
    role: str,
) -> set[str]:

    return ROLE_PERMISSIONS.get(
        role,
        set(),
    )