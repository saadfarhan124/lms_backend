from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import CustomerCreate, Customer, Individual
from app.database.database import get_db
from app.utils import customer as customer_crud, email_address_crud, employer_crud, address_crud, mobile_number_crud, individual_crud
from app.constants import CustomerType

router = APIRouter()


@router.post("/customers/individual", response_model=Individual)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    cust_obj = customer_crud.create(db, create_schema=customer)
    if cust_obj.user_type == CustomerType.INDIVIDUAL.value:
        customer.individual.customer_id = cust_obj.id
        individual_obj = individual_crud.create(
            db, create_schema=customer.individual)
        customer.individual.employer.individual_id = individual_obj.id
        employer_obj = employer_crud.create(
            db, create_schema=customer.individual.employer)
        customer.individual.address.individual_id = individual_obj.id
        address_obj = address_crud.create(
            db, create_schema=customer.individual.address)
        mobile_numbers, email_addresses = [], []
        for email_address in customer.individual.email_addresses:
            email_address.individual_id = individual_obj.id
            email_addresses.append(email_address_crud.create(
                db, create_schema=email_address))
        for mobile_number in customer.individual.mobile_numbers:
            mobile_number.individual_id = individual_obj.id
            mobile_numbers.append(mobile_number_crud.create(
                db, create_schema=mobile_number))
        individual_obj.marital_status_string = "individual_obj.marital_status_string"
        return individual_obj


@router.get("/customers/individual/{user_id}", response_model=Individual)
def get_individual_customer(user_id: int, db: Session = Depends(get_db)):
    return individual_crud.get(db, id=user_id)

# Get All Customers Individual


@router.get("/customers/individual/{offset}/{limit}", response_model=List[Individual])
def get_all_individual_customers(offset: int, limit: int, db: Session = Depends(get_db)):
    return individual_crud.get_multi(db, offset=offset, limit=limit)

    # Update Address
    # Update Employer
    # Create Customer Business
    # Get Customer Business By ID
    # Get All Customers Business

    # Delete Customer Individual
    # Delete Customer Business
