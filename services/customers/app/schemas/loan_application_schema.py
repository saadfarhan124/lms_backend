from pydantic import BaseModel, validator
from decimal import Decimal
from app.constants import is_valid_term_mode, is_valid_payment_mode
from app.constants import get_loan_type_string, get_loan_status_string, get_term_modes_string, get_mode_of_payments_string
from typing import List, Union
from datetime import date
from app.schemas import Customer, Individual, Business


#
class LoanApplicationChequesCreate(BaseModel):
    loan_application_id: Union[None, int]
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


class GuarantorCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    mobile_number: str
    address: str
    employer_name: str
    employer_email: str
    employer_number: str
    employer_address: str


class GuarantorUpdate(GuarantorCreate):
    id: int


class Guarantor(GuarantorUpdate):
    formatted_date_str: str = None

    @validator("formatted_date_str", always=True)
    def get_formatted_date(cls, v, values, **kwargs):
        # Assuming the date_of_birth value is a string
        date_of_birth = values["date_of_birth"]
        # Determine the day suffix
        day = date_of_birth.day
        if day in (1, 21, 31):
            suffix = "st"
        elif day in (2, 22):
            suffix = "nd"
        elif day in (3, 23):
            suffix = "rd"
        else:
            suffix = "th"

        # # Format the date
        formatted_date = date_of_birth.strftime(f"%d{suffix} %b, %Y")
        return f"{formatted_date}"

    class Config:
        orm_mode = True


class GuarantorsList(BaseModel):
    guarantors: List[Guarantor]
    count: int

#


class LoanApplicationPaymentScheduleCreate(BaseModel):
    loan_application_id: Union[None, int]
    # loan_application_id: Union[None, int]
    loan_repayment_amount: Union[None, Decimal]
    principal_paid: Union[None, Decimal]
    payment_date: date
    bagging_balance: Decimal
    balance: Decimal
    interest_paid: Decimal


class LoanApplicationPaymentScheduleUpdate(LoanApplicationPaymentScheduleCreate):
    id: int


class LoanApplicationPaymentSchedule(LoanApplicationPaymentScheduleUpdate):
    class Config:
        orm_mode = True

#


class LoanApplicationCreate(BaseModel):
    customer_id: int
    guarantors: List[int]
    co_borrowers: Union[None, List[int]]
    cheques: Union[None, List[LoanApplicationChequesCreate]]
    schedules: List[LoanApplicationPaymentScheduleCreate]
    fees: Union[None, List[FeesCreate]]
    date_applied: date
    purpose: str
    principal_amount: Decimal
    interest_rate: Decimal
    interest_rate_is_flat: bool
    o_and_s_rate: Decimal
    loan_repayment_amount: Union[Decimal, None]
    o_and_s_rate_is_flat: bool
    length: int
    term: int
    status: Union[None, int]
    loan_type: int
    mode_of_payment: int

    @validator("term")
    def validate_term(cls, term, values, **kwargs):
        if not is_valid_term_mode(term):
            raise ValueError("Not a valid term mode")
        return term

    @validator("mode_of_payment")
    def validate_mode_of_payment(cls, mode_of_payment, values, **kwargs):
        if not is_valid_payment_mode(mode_of_payment):
            raise ValueError("Not a valid mode of payment")
        return mode_of_payment

    @validator("guarantors")
    def validate_guarantors(cls, guarantors, values, **kwargs):
        if len(guarantors) <= 0:
            raise ValueError("There needs to be at least one guarantor")
        return guarantors

    @validator("schedules")
    def validate_schedules(cls, schedules, values, **kwargs):
        if len(schedules) <= 0:
            raise ValueError("There needs to be at least one payment schedule")
        return schedules


class LoanApplicationUpdate(LoanApplicationCreate):
    id: int


class LoanApplication(LoanApplicationUpdate):
    # customers: CustomerTest
    guarantors: List[Guarantor]
    co_borrowers: Union[None, List[Customer]]
    cheques: Union[None, List[LoanApplicationCheques]]
    fees: Union[None, List[Fees]]
    schedules: List[LoanApplicationPaymentSchedule]
    formatted_date_str: str = None
    loan_type_string: str = None
    status_string: str = None
    term_string: str = None
    payment_mode_string: str = None

    @validator("payment_mode_string", always=True)
    def get_payment_mode_string(cls, v, values, **kwargs):
        return f"{get_mode_of_payments_string(values['mode_of_payment'])}"
    
    @validator("term_string", always=True)
    def get_term_string(cls, v, values, **kwargs):
        return f"{get_term_modes_string(values['term'])}"

    @validator("loan_type_string", always=True)
    def get_loan_type_string(cls, v, values, **kwargs):
        return f"{get_loan_type_string(values['loan_type'])}"

    @validator("status_string", always=True)
    def get_status_string(cls, v, values, **kwargs):
        return f"{get_loan_status_string(values['status'])}"

    @validator("formatted_date_str", always=True)
    def get_formatted_date(cls, v, values, **kwargs):
        # Assuming the date_of_birth value is a string
        date_applied = values["date_applied"]
        return f'{date_applied.strftime(f"%d-%m-%Y")}'

    class Config:
        orm_mode = True


class LoanApplicationList(BaseModel):
    loan_applications: List[LoanApplication]
    count: int

#


class PaymentSchedule(BaseModel):
    current_date: date
    total_amount: Union[None, Decimal]
    loan_repayment_amount: Union[None, Decimal]
    num_payments: int
    term_mode: int
    principal_amount: Union[None, Decimal]
    interest_rate: Union[None, Decimal]
    interest_amount: Union[None, Decimal]
    interest_rate_is_flat: Union[None, bool]
    o_and_s_rate: Union[None, Decimal]
    o_and_s_amount: Union[None, Decimal]
    o_and_s_rate_is_flat: Union[None, bool]

#


class PreDefinedFeesCreate(BaseModel):
    title: str


class PreDefinedFeesUpdate(PreDefinedFeesCreate):
    id: int


class PreDefinedFees(PreDefinedFeesUpdate):
    class Config:
        orm_mode = True


class ScheduleReturn(BaseModel):
    schedule: List[LoanApplicationPaymentScheduleCreate]
    breakdown: PaymentSchedule


class LoanApplicationWithCustomer(BaseModel):
    loan_application: LoanApplication
    customer: Individual

class LoanApplicationWithCustomerIndividual(LoanApplicationWithCustomer):
    customer: Individual

class LoanApplicationWithCustomerBusiness(LoanApplicationWithCustomer):
    customer: Business