from enum import Enum
class MaritalStatus(Enum):
    SINGLE = 1
    MARRIED = 2
    DIVORCED = 3
    WIDOWED = 4


def get_marital_status_string(marital_status: int) -> str:
    if marital_status == MaritalStatus.SINGLE.value:
        return "Single"
    elif marital_status == MaritalStatus.MARRIED.value:
        return "Married"
    elif marital_status == MaritalStatus.DIVORCED.value:
        return "Divorced"
    elif marital_status == MaritalStatus.WIDOWED.value:
        return "Widowed"
    return "unknown"

def get_marital_status_enum(marital_status: str) -> MaritalStatus:
    if marital_status.lower() == "single":
        return MaritalStatus.SINGLE
    elif marital_status.lower() == "married":
        return MaritalStatus.MARRIED
    elif marital_status.lower() == "divorced":
        return MaritalStatus.DIVORCED
    elif marital_status.lower() == "widowed":
        return MaritalStatus.WIDOWED
    raise ValueError("Invalid Marital status string") 