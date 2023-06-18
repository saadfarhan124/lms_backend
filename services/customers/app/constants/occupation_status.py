from enum import Enum
class OccupationStatus(Enum):
    EMPLOYED = 1
    SELF_EMPLOYED = 2
    UNEMPLOYED = 3

def get_occupation_status_string(occupation_status: int) -> str:
    if occupation_status == OccupationStatus.EMPLOYED.value:
        return "Employed"
    elif occupation_status == OccupationStatus.SELF_EMPLOYED.value:
        return "Self Employed"
    elif occupation_status == OccupationStatus.UNEMPLOYED.value:
        return "Unemployed"
    return "unknown"

def get_occupation_status_enum(occupation_status_string: str) -> OccupationStatus:
    if occupation_status_string.lower() == "employed":
        return OccupationStatus.EMPLOYED
    elif occupation_status_string.lower() == "self employed":
        return OccupationStatus.SELF_EMPLOYED
    elif occupation_status_string.lower() == "unemployed":
        return OccupationStatus.UNEMPLOYED
    raise ValueError("Invalid occupation string")