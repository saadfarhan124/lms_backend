from enum import Enum
class ModeOfPayments(Enum):
    CASH = 1
    CHECK = 2
    WAGE_GARNISHMENT = 3
    STANDING_ORDER = 4
    OTHER = 5



def get_mode_of_payments_string(mode_of_payment: int) -> str:
    if mode_of_payment == ModeOfPayments.CASH.value:
        return "Cash"
    elif mode_of_payment == ModeOfPayments.CHECK.value:
        return "Check"
    elif mode_of_payment == ModeOfPayments.WAGE_GARNISHMENT.value:
        return "Wage Garnishment"
    elif mode_of_payment == ModeOfPayments.STANDING_ORDER.value:
        return "Standing Order"
    elif mode_of_payment == ModeOfPayments.OTHER.value:
        return "Other"
    return "unknown"

def get_mode_of_payment_enum(marital_status: str) -> ModeOfPayments:
    if marital_status.lower() == "cash":
        return ModeOfPayments.CASH
    elif marital_status.lower() == "check":
        return ModeOfPayments.CASH
    elif marital_status.lower() == "wage garnishment":
        return ModeOfPayments.WAGE_GARNISHMENT
    elif marital_status.lower() == "standing order":
        return ModeOfPayments.STANDING_ORDER
    elif marital_status.lower() == "other":
        return ModeOfPayments.OTHER
    raise ValueError("Invalid Mode of Payment string") 