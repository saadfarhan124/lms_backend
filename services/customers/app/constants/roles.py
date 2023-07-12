from enum import Enum


class Roles(Enum):
    MANAGING_DIRECTOR = 1
    LOANS_MANAGER = 2
    PROJECT_MANAGER = 3
    LOANS_ASSOCIATE = 4
    LOANS_ANALYST = 5


def get_roles_strings() -> str:
    roles = {
        role.name.replace("_", " ").title(): role.value
        for role in Roles
    }
    return roles



def is_valid_role(role_int: int) -> bool:
    return any(role_int == role.value for role in Roles)