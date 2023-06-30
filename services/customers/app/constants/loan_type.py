from enum import Enum

class LoanType(Enum):
    PERSONAL = 1
    VEHICLE = 2

def get_loan_type_string(loan_type: int) -> str:
    if loan_type == LoanType.PERSONAL.value:
        return "Personal"
    elif loan_type == LoanType.VEHICLE.value:
        return "Vehicle"
    return "unknown"

def get_loan_type(loan_type: str) -> LoanType:
    if loan_type.lower() == "personal":
        return LoanType.PERSONAL
    elif loan_type.lower() == "vehicle":
        return LoanType.VEHICLE
    raise ValueError("Invalid Loan Type")