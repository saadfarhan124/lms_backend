from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import CustomerCreate, Individual, AddressUpdate, EmployerUpdate, BussinessCustomerCreate, Business, BussinessUpdate
from app.database.database import get_db
from app.utils import customer as customer_crud, email_address_crud, employer_crud, address_crud, mobile_number_crud, individual_crud, bussiness_crud

router = APIRouter()


@router.post("/customers/individual", response_model=Individual)
def create_individual_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    
    cust_obj = customer_crud.create(db, create_schema=customer)
    customer.individual.customer_id = cust_obj.id
    individual_obj = individual_crud.create(
        db, create_schema=customer.individual)
    customer.individual.employer.individual_id = individual_obj.id
    employer_crud.create(
        db, create_schema=customer.individual.employer)
    customer.individual.address.individual_id = individual_obj.id
    address_crud.create(
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
    return individual_obj


@router.get("/customers/individual/{user_id}", response_model=Individual)
def get_individual_customer(user_id: int, db: Session = Depends(get_db)):
    return individual_crud.get(db, id=user_id)

# Get All Customers Individual
@router.get("/customers/individual/{offset}/{limit}", response_model=List[Individual])
def get_all_individual_customers(offset: int, limit: int, db: Session = Depends(get_db)):
    return individual_crud.get_multi(db, offset=offset, limit=limit)

# Update Address
@router.put("/customers/individual/address")
def update_customer_address(address: AddressUpdate, db:Session = Depends(get_db)):
    address_obj = address_crud.get(db, id=address.id)
    return address_crud.update(db, db_obj=address_obj, update_schema=address)
    
# Update Employer
@router.put("/customers/individual/employer")
def update_customer_individual(employer: EmployerUpdate, db:Session = Depends(get_db)):
    employer_obj = employer_crud.get(db, id=employer.id)
    return employer_crud.update(db, db_obj=employer_obj, update_schema=employer)
    
# Create Customer Business
@router.post("/customers/business", response_model=Business)
def create_customer_business(customer: BussinessCustomerCreate, db: Session = Depends(get_db)):
    cust_obj = customer_crud.create(db, create_schema=customer)
    customer.business.customer_id = cust_obj.id
    business_obj = bussiness_crud.create(db, create_schema=customer.business)
    return business_obj


# Get Customer Business By ID
@router.get("/customers/business/{id}", response_model=Business)
def get_business_by_id(id: int, db: Session = Depends(get_db)):
    return  bussiness_crud.get(db, id=id)

# Get All Customers Business
@router.get("/customers/business/{offset}/{limit}", response_model=List[Business])
def get_all_businesses(offset: int, limit: int, db: Session= Depends(get_db)):
    return bussiness_crud.get_multi(db, offset=offset, limit=limit)

# Update Business
@router.put("/customers/business")
def update_business(business: BussinessUpdate, db: Session = Depends(get_db)):
    business_obj = bussiness_crud.get(db, wid=business.id)
    return bussiness_crud.update(db, db_obj=business_obj, update_schema=business
                                 )
# Delete Customer Individual
# Delete Customer Business
