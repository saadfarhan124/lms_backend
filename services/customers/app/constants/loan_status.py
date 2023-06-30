from enum import Enum

class LoanStatus(Enum):
    UNAPPROVED = 1
    APPROVED = 2
    AMMEND = 3
    DECLINED = 4
    WITHDRAW = 5
    PRE_CLOSE = 6
    CLOSE = 7
    ACTIVE_LOAN = 8


def get_loan_status_string(loan_status: int) -> str:
    if loan_status == LoanStatus.UNAPPROVED.value:
        return "Unapproved"
    elif loan_status == LoanStatus.APPROVED.value:
        return "Approved"
    elif loan_status == LoanStatus.AMMEND.value:
        return "Ammend"
    elif loan_status == LoanStatus.DECLINED.value:
        return "Declined"
    elif loan_status == LoanStatus.WITHDRAW.value:
        return "Withdraw"
    elif loan_status == LoanStatus.PRE_CLOSE.value:
        return "Pre Close"
    elif loan_status == LoanStatus.CLOSE.value:
        return "Close"
    elif loan_status == LoanStatus.ACTIVE_LOAN.value:
        return "Active Loan"
    return "unknown"

def get_loan_status_enum(loan_status: str) -> LoanStatus:
    if loan_status.lower() == "unapproved":
        return LoanStatus.UNAPPROVED
    elif loan_status.lower() == "approved":
        return LoanStatus.APPROVED
    elif loan_status.lower() == "ammend":
        return LoanStatus.AMMEND
    elif loan_status.lower() == "declined":
        return LoanStatus.DECLINED
    elif loan_status.lower() == "withdraw":
        return LoanStatus.WITHDRAW
    elif loan_status.lower() == "pre close":
        return LoanStatus.PRE_CLOSE
    elif loan_status.lower() == "close":
        return LoanStatus.CLOSE
    elif loan_status.lower() == "active loan":
        return LoanStatus.ACTIVE_LOAN
    raise ValueError("Invalid Loan Status string")