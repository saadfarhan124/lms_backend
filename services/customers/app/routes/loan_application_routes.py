from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Union, Dict, Any, List
from app.schemas import LoanApplicationCreate, LoanApplication
from app.schemas import GuarantorCreate, GuarantorUpdate, Guarantor, GuarantorsList
from app.schemas import LoanApplicationPaymentScheduleCreate
from app.schemas import PaymentSchedule, ScheduleReturn
from decimal import Decimal, ROUND_HALF_UP
from app.database.database import get_db
from app.utils import loan_application_crud, loan_application_cheques_crud, loan_application_payment_schedule_crud, guarantor_crud, fees_crud, predefined_fees_crud
from app.utils import customer as customer_crud
from app.utilities import get_tracback
from app.constants import TermModes, get_term_modes_string, ModeOfPayments, get_mode_of_payments_string
from datetime import datetime, timedelta
from pydantic import ValidationError


router = APIRouter()


@router.post('/loan_application', response_model=LoanApplication)
def create_loan_application(loan_application: LoanApplicationCreate, db: Session = Depends(get_db)):
    loan_application_obj = None
    try:
        interest_rate = loan_application.principal_amount * \
            (loan_application.interest_rate /
             100) if not loan_application.interest_rate_is_flat else loan_application.interest_rate
        o_and_s_rate = loan_application.principal_amount * \
            (loan_application.o_and_s_rate /
             100) if not loan_application.o_and_s_rate_is_flat else loan_application.o_and_s_rate
        loan_repayment_amount: Decimal = (
            loan_application.principal_amount + interest_rate + o_and_s_rate) / loan_application.length
        loan_application.loan_repayment_amount = loan_repayment_amount.quantize(
            Decimal('0.00'), rounding=ROUND_HALF_UP)
        loan_application_obj = loan_application_crud.create(
            db, create_schema=loan_application)

        # Co Borrowers
        if loan_application.co_borrowers is not None and len(loan_application.co_borrowers) > 0:
            co_borrowers = customer_crud.get_by_ids(
                db, ids=loan_application.co_borrowers)
            for co_borrower in co_borrowers:
                loan_application_obj.co_borrowers.append(co_borrower)

        # Guarantors
        guarantors = guarantor_crud.get_by_ids(
            db, ids=loan_application.guarantors)
        for guarantor in guarantors:
            print(guarantor.address)
            loan_application_obj.guarantors.append(guarantor)

        # Cheques
        if loan_application.cheques is not None and len(loan_application.cheques) > 0:
            for cheque in loan_application.cheques:
                cheque.loan_application_id = loan_application_obj.id
                loan_application_cheques_crud.create(db, create_schema=cheque)

        # Fees
        if loan_application.fees is not None and len(loan_application.fees) > 0:
            for fee in loan_application.fees:
                fee_obj = fees_crud.create(db, create_schema=fee)
                loan_application_obj.fees.append(fee_obj)

        # Payment Schedules
        for schedule in loan_application.schedules:
            schedule.loan_application_id = loan_application_obj.id
            loan_application_payment_schedule_crud.create(
                db, create_schema=schedule)

        db.add(loan_application_obj)
        db.commit()
        db.refresh(loan_application_obj)

        return loan_application_obj
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())


@router.post("/payment_schedule", response_model=ScheduleReturn)
def get_payment_schedule(payment_schedule: PaymentSchedule):
    try:
        interest_rate = payment_schedule.principal_amount * \
            (payment_schedule.interest_rate /
             100) if not payment_schedule.interest_rate_is_flat else payment_schedule.interest_rate
        interest_rate = interest_rate.quantize(
            Decimal('0.00'), rounding=ROUND_HALF_UP)
        o_and_s_rate = payment_schedule.principal_amount * \
            (payment_schedule.o_and_s_rate /
             100) if not payment_schedule.o_and_s_rate_is_flat else payment_schedule.o_and_s_rate
        o_and_s_rate = o_and_s_rate.quantize(
            Decimal('0.00'), rounding=ROUND_HALF_UP)
        loan_repayment_amount: Decimal = ((
            payment_schedule.principal_amount + interest_rate + o_and_s_rate) / payment_schedule.num_payments).quantize(
            Decimal('0.00'), rounding=ROUND_HALF_UP)
        payment_schedule.loan_repayment_amount = loan_repayment_amount

        payment_schedule.total_amount = interest_rate + \
            o_and_s_rate + payment_schedule.principal_amount
        payment_schedule.interest_amount = interest_rate
        payment_schedule.o_and_s_amount = o_and_s_rate

        interest_paid = (loan_repayment_amount / payment_schedule.num_payments).quantize(
            Decimal('0.00'), rounding=ROUND_HALF_UP)
        principal_paid = (loan_repayment_amount - interest_paid).quantize(
            Decimal('0.00'), rounding=ROUND_HALF_UP)
        payment_date = payment_schedule.current_date

        bagging_balance = payment_schedule.total_amount
        balance = payment_schedule.total_amount - \
            payment_schedule.loan_repayment_amount
        if payment_schedule.term_mode == TermModes.WEEKS.value:
            term_delta = timedelta(weeks=1)
        elif payment_schedule.term_mode == TermModes.MONTHS.value:
            term_delta = timedelta(days=30)  # Assuming 30 days in a month
        elif payment_schedule.term_mode == TermModes.FORTNIGHTLY.value:
            term_delta = timedelta(weeks=2)

        payment_schedule_list: List[LoanApplicationPaymentScheduleCreate] = []
        for i in range(1, payment_schedule.num_payments + 1):
            payment_schedule_obj = LoanApplicationPaymentScheduleCreate(
                payment_date=payment_date,
                bagging_balance=Decimal(str(bagging_balance)),
                balance=Decimal(str(balance)),
                interest_paid=Decimal(str(interest_paid)),
                loan_repayment_amount=loan_repayment_amount,
                principal_paid=principal_paid)

            payment_schedule_list.append(payment_schedule_obj)
            next_payment_date = payment_date + term_delta
            if payment_schedule.term_mode == TermModes.MONTHS.value:
                while next_payment_date.day != payment_date.day:
                    next_payment_date += timedelta(days=1)
            payment_date = next_payment_date
            bagging_balance -= payment_schedule.loan_repayment_amount
            balance -= payment_schedule.loan_repayment_amount

        return ScheduleReturn(breakdown=payment_schedule, schedule=payment_schedule_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())


# Guarantor Endpoints
@router.post('/guarantor', response_model=Guarantor)
def create_guarantor(guarantor: GuarantorCreate, db: Session = Depends(get_db)):
    gurantor_obj = guarantor_crud.create(db, create_schema=guarantor)
    return gurantor_obj


@router.get("/guarantor/{guarantor_id}", response_model=Guarantor)
def get_guarantor_by_id(guarantor_id: int, db: Session = Depends(get_db)):
    return guarantor_crud.get(db, id=guarantor_id)


@router.get("/guarantors/{offset}/{limit}", response_model=GuarantorsList)
def get_all_guarantors(offset: int, limit: int, db: Session = Depends(get_db)):
    return GuarantorsList(guarantors=guarantor_crud.get_multi(db, offset=offset, limit=limit), count=guarantor_crud.get_count(db))


@router.get("/guarantors", response_model=List[Guarantor])
def get_all_guarantors(db: Session = Depends(get_db)):
    return guarantor_crud.get_all(db)


@router.put("/guarantor", response_model=Guarantor)
def update_gurantor(guarantor: GuarantorUpdate, db: Session = Depends(get_db)):
    guarantor_obj = guarantor_crud.get(db, id=guarantor.id)
    return guarantor_crud.update(db, db_obj=guarantor_obj, update_schema=guarantor)


# Utils
@router.get("/loan-application/term-modes")
def get_term_modes():
    term_modes = [
        {"key": bt.value, "value": get_term_modes_string(bt.value)}
        for bt in TermModes
    ]
    return {"data": term_modes}


@router.get("/loan-application/payment-modes")
def get_mode_pf_payments():
    term_modes = [
        {"key": bt.value, "value": get_mode_of_payments_string(bt.value)}
        for bt in ModeOfPayments
    ]
    return {"data": term_modes}
