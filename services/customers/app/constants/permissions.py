from enum import Enum


class Permissions(Enum):
    ADD_USER = 1
    DELETE_USER = 2
    SET_USER_PERMISSIONS = 3
    TRACK_USER_ACTIVITY = 4
    APPROVE_CREDIT_MEMO = 5
    # VIEW_DASHBOARD_STATISTICS = 6
    REPORTS = 7
    ACCOUNTING = 8
    APPROVE_REVERSED_PAYMENTS = 9
    VIEW_STATISTICS = 10
    VIEW_REPORTS = 11
    ADD_PAYMENTS = 12
    ADD_CUSTOMER = 13
    ADD_LOAN_APPLICATION = 14


def get_permission_strings() -> str:
    permissions = {
        permission.name.replace("_", " ").title(): permission.value
        for permission in Permissions
    }
    return permissions

def get_permission_string(id: int) -> str:
    for perm in Permissions:
        if id == perm.value:
            return perm.name.replace("_", " ").title()

def is_valid_permission(permission_int: int) -> bool:
    return any(permission_int == permission.value for permission in Permissions)