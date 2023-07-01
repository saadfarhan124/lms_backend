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
    

class LoanApplicationUpdate(LoanApplicationCreate):
    pass

class LoanApplication(LoanApplicationUpdate):
    class Config:
        orm_mode = True

# 
class GuarantorCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    mobile_number: str
    address: str
    employer_name: str
    employer_email: str
    employer_email: str
    employer_address: str

class GuarantorUpdate(GuarantorCreate):
    id: int

class Guarantor(GuarantorUpdate):
    class Config:
        orm_mode = True

# 
class LoanApplicationPaymentScheduleCreate(BaseModel):
    pass

class LoanApplicationPaymentScheduleUpdate(LoanApplicationPaymentScheduleCreate):
    id: int

class LoanApplicationPaymentSchedule(LoanApplicationPaymentScheduleUpdate):
    class Config:
        orm_mode  = True


# 
class LoanApplicationChequesCreate(BaseModel):
    bank: str
    branch: str
    cheque_no: str
    date: date
    amount: Decimal
    
class LoanApplicationChequesUpdate(LoanApplicationChequesCreate):
    id: int

class LoanApplicationCheques(LoanApplicationChequesUpdate):
    class Config:
        orm_mode = True

# 
class FeesCreate(BaseModel):
    title: str
    amount: Decimal

class FeesUpdate(FeesCreate):
    id: int

class Fees(FeesUpdate):
    class Config:
        orm_mode = True


# 

class PreDefinedFeesCreate(BaseModel):
    title: str

class PreDefinedFeesUpdate(PreDefinedFeesCreate):
    id: int

class PreDefinedFees(PreDefinedFeesUpdate):
    class Config:
        orm_mode = True