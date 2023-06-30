from pydantic import BaseModel, validator
from decimal import Decimal
from app.constants import is_valid_term_mode, is_valid_payment_mode
# from typing import 
from datetime import date

class LoanApplicationCreate(BaseModel):
    date_applied: date
    purpose: str
    principal_amount: Decimal
    interest_rate: Decimal
    interest_rate_flat: bool
    o_and_s_rate: Decimal
    o_and_s_rate_flat: bool
    length: int
    term_mode: int
    loan_type: int
    mode_of_payment: int
    
    @validator("term_mode")
    def validate_term(cls, term_mode, values, **kwargs):
        if not is_valid_term_mode(term_mode):
            raise ValueError("Not a valid term mode")
        return term_mode
    
    @validator("mode_of_payment")
    def validate_mode_of_payment(cls, mode_of_payment, values, **kwargs):
        if not is_valid_payment_mode(mode_of_payment):
            raise ValueError("Not a valid mode of payment")
        return mode_of_payment