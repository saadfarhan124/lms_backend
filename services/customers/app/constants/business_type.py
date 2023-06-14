from enum import Enum

class BusinessType(Enum):
    SOLE_PROPRIETORSHIP = 1
    PARTNERSHIP = 2
    CORPORATION = 3
    LLC = 4

def get_business_type_string(business_type: BusinessType) -> str:
    if business_type == BusinessType.SOLE_PROPRIETORSHIP.value:
        return "Sole Proprietorship"
    elif business_type == BusinessType.PARTNERSHIP.value:
        return "Partnership"
    elif business_type == BusinessType.CORPORATION.value:
        return "Corporation"
    elif business_type == BusinessType.LLC.value:
        return "LLC"
    return "unknown"

def get_business_type_enum(business_type: str) -> BusinessType:
    if business_type.lower() == "sole proprietorship":
        return BusinessType.SOLE_PROPRIETORSHIP
    elif business_type.lower() == "partnership":
        return BusinessType.PARTNERSHIP
    elif business_type.lower() == "corporation":
        return BusinessType.CORPORATION
    elif business_type.lower() == "llc":
        return BusinessType.LLC
    raise ValueError("Invalid Business type string")