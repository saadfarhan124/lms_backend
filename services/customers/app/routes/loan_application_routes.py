from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Union, Dict, Any, List
from app.schemas import LoanApplicationCreate, LoanApplication
from app.schemas import GuarantorCreate, GuarantorUpdate, Guarantor, GuarantorsList
from decimal import Decimal, ROUND_HALF_UP
from app.database.database import get_db
from app.utils import loan_application_crud, loan_application_cheques_crud, loan_application_payment_schedule_crud, guarantor_crud, fees_crud, predefined_fees_crud
from app.utils import customer as customer_crud
from app.utilities import get_tracback
from pydantic import ValidationError


router = APIRouter()


@router.post('/loan_application', response_model=LoanApplication)
def create_loan_application(loan_application: LoanApplicationCreate, db: Session = Depends(get_db)):
    loan_application_obj = None
    try:
        interest_rate = loan_application.principal_amount * (loan_application.interest_rate / 100) if not loan_application.interest_rate_is_flat else loan_application.interest_rate
        o_and_s_rate = loan_application.principal_amount * (loan_application.o_and_s_rate / 100) if not loan_application.o_and_s_rate_is_flat else loan_application.o_and_s_rate
        loan_repayment_amount: Decimal = (loan_application.principal_amount + interest_rate + o_and_s_rate) / loan_application.length
        loan_application.loan_repayment_amount = loan_repayment_amount.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        loan_application_obj = loan_application_crud.create(db, create_schema=loan_application)

        # Co Borrowers
        if loan_application.co_borrowers is not None and len(loan_application.co_borrowers) > 0:
            co_borrowers = customer_crud.get_by_ids(db, ids=loan_application.co_borrowers)
            for co_borrower in co_borrowers:
                loan_application_obj.co_borrowers.append(co_borrower)
        
        # Guarantors
        guarantors = guarantor_crud.get_by_ids(db, ids=loan_application.guarantors)
        for guarantor in guarantors:
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
                
        db.add(loan_application_obj)
        db.commit()
        db.refresh(loan_application_obj)
        
        return loan_application_obj
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
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
def get_all_guarantors(offset: int, limit: int, db:Session = Depends(get_db)):
    return GuarantorsList(guarantors=guarantor_crud.get_multi(db, offset=offset, limit=limit), count = guarantor_crud.get_count(db))

@router.put("/guarantor", response_model=Guarantor)
def update_gurantor(guarantor: GuarantorUpdate, db: Session = Depends(get_db)):
    guarantor_obj = guarantor_crud.get(db, id=guarantor.id)
    return guarantor_crud.update(db, db_obj=guarantor_obj, update_schema=guarantor)