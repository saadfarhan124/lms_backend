from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import LoanApplicationCreate
from app.schemas import GuarantorCreate, GuarantorUpdate, Guarantor, GuarantorsList
from decimal import Decimal, ROUND_HALF_UP
from app.database.database import get_db
from app.utils import loan_application_crud, loan_application_cheques_crud, loan_application_payment_schedule_crud, guarantor_crud, fees_crud, predefined_fees_crud


router = APIRouter()


@router.post('/loan_application')
def create_loan_application(loan_application: LoanApplicationCreate, db: Session = Depends(get_db)):

    interest_rate = loan_application.principal_amount * (loan_application.interest_rate / 100) if not loan_application.interest_rate_flat else loan_application.interest_rate
    o_and_s_rate = loan_application.principal_amount * (loan_application.o_and_s_rate / 100) if not loan_application.o_and_s_rate_flat else loan_application.o_and_s_rate
    
    loan_repayment_amount: Decimal = (loan_application.principal_amount + interest_rate + o_and_s_rate) / loan_application.length

    formatted_result = loan_repayment_amount.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)




    return {"Hello ": "World"}


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