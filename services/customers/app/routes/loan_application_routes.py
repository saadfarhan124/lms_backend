from fastapi import APIRouter
from app.schemas import LoanApplicationCreate
from app.constants import TermModes
from decimal import Decimal, ROUND_HALF_UP

router = APIRouter()


@router.post('/loan_application')
def create_loan_application(loan_application: LoanApplicationCreate):

    interest_rate = loan_application.principal_amount * (loan_application.interest_rate / 100) if not loan_application.interest_rate_flat else loan_application.interest_rate
    o_and_s_rate = loan_application.principal_amount * (loan_application.o_and_s_rate / 100) if not loan_application.o_and_s_rate_flat else loan_application.o_and_s_rate
    
    loan_repayment_amount: Decimal = (loan_application.principal_amount + interest_rate + o_and_s_rate) / loan_application.length

    formatted_result = loan_repayment_amount.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    print(formatted_result)
    return {"Hello ": "World"}


# b5 = Principal Amount
# b6 = O and S rate Percentage
# b7 = Interest Rate Percentage
# b8 = Length
# result = (b5 + (b5 * b6) + (b5 * b7)) / b8

# e5 = Principal Amoubnt
# e6 = O and S Rate Flat
# e7 = Interest Rate Percentage
# e8 = Length
# result = (e5 + e6 + (e5 * e7)) / e8
