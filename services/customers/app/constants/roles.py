from enum import Enum
from . import Permissions

class Roles(Enum):
    MANAGING_DIRECTOR = 1
    LOANS_MANAGER = 2
    PROJECT_MANAGER = 3
    LOANS_ASSOCIATE = 4
    LOANS_ANALYST = 5


role_permissions = {
    Roles.MANAGING_DIRECTOR.value: [
        Permissions.ADD_USER.value,
        Permissions.DELETE_USER.value,
        Permissions.SET_USER_PERMISSIONS.value,
        Permissions.TRACK_USER_ACTIVITY.value,
        Permissions.APPROVE_CREDIT_MEMO.value,
        Permissions.VIEW_STATISTICS.value,
        Permissions.REPORTS.value,
        Permissions.ACCOUNTING.value,
    ],
    Roles.LOANS_MANAGER.value: [
        Permissions.APPROVE_CREDIT_MEMO.value,
        Permissions.APPROVE_REVERSED_PAYMENTS.value,
        Permissions.VIEW_STATISTICS.value,
        Permissions.REPORTS.value,
        Permissions.ADD_PAYMENTS.value,
        # To Do Assign Tasks
        # Permissions.AssignTasks,       
    ],
    Roles.PROJECT_MANAGER.value: [
        Permissions.VIEW_STATISTICS.value,
        Permissions.REPORTS.value,
        Permissions.ACCOUNTING.value
    ],

    Roles.LOANS_ASSOCIATE.value: [
        Permissions.ADD_CUSTOMER.value,
        Permissions.ADD_LOAN_APPLICATION.value,
        Permissions.ADD_PAYMENTS.value,
        Permissions.ACCOUNTING.value,
    ],
    Roles.LOANS_ANALYST.value: [
        Permissions.ADD_CUSTOMER.value,
        Permissions.ADD_LOAN_APPLICATION.value,
        Permissions.ADD_PAYMENTS.value,
    ]
}


def get_roles_strings() -> str:
    roles = {
        role.name.replace("_", " ").title(): role.value
        for role in Roles
    }
    return roles



def is_valid_role(role_int: int) -> bool:
    return any(role_int == role.value for role in Roles)