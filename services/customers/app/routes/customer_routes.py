from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import CustomerCreate, Individual, IndividualList, IndividualUpdate, AddressUpdate, EmployerUpdate
from app.schemas import BussinessCustomerCreate, Business, BussinessUpdate, BusinessList
from app.schemas import EmailAddressDelete, MobileNumberDelete
from app.database.database import get_db
from app.utils import customer as customer_crud, email_address_crud, employer_crud, address_crud, mobile_number_crud, individual_crud, bussiness_crud
from app.constants import BusinessType, get_business_type_string, OccupationStatus, get_occupation_status_string, MaritalStatus, get_marital_status_string, Gender, get_gender_string

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

# Get Customer Individual By ID


@router.get("/customers/individual/{user_id}", response_model=Individual)
def get_individual_customer(user_id: int, db: Session = Depends(get_db)):
    return individual_crud.get(db, id=user_id)

# Get All Customers Individual


@router.get("/customers/individual/{offset}/{limit}", response_model=IndividualList)
def get_all_individual_customers(offset: int, limit: int, db: Session = Depends(get_db)):
    return IndividualList(customers=individual_crud.get_multi(db, offset=offset, limit=limit), count=individual_crud.get_count(db))

# Update Customer Personal Informatin


@router.put("/customers/individual", response_model=Individual)
def update_individual(individual: IndividualUpdate, db: Session = Depends(get_db)):
    for email in individual.email_addresses:
        email_obj = email_address_crud.get(db=db, id=email.id)
        email_address_crud.update(db, db_obj=email_obj, update_schema=email)
    for number in individual.mobile_numbers:
        number_obj = mobile_number_crud.get(db=db, id=number.id)
        mobile_number_crud.update(db, db_obj=number_obj, update_schema=number)
    individual_obj = individual_crud.get(db, id=individual.id)
    # TO DO Configure remove and add new email address and mobile number case

    return individual_crud.update(db, db_obj=individual_obj, update_schema=individual)

# Update Address
@router.put("/customers/individual/address")
def update_customer_address(address: AddressUpdate, db: Session = Depends(get_db)):
    address_obj = address_crud.get(db, id=address.id)
    return address_crud.update(db, db_obj=address_obj, update_schema=address)

# Update Employer
@router.put("/customers/individual/employer")
def update_customer_individual(employer: EmployerUpdate, db: Session = Depends(get_db)):
    employer_obj = employer_crud.get(db, id=employer.id)
    return employer_crud.update(db, db_obj=employer_obj, update_schema=employer)


# Delete Email Address
@router.delete("/customers/email_address")
def delete_email_address(email_address: EmailAddressDelete, db: Session = Depends(get_db)):
    return email_address_crud.remove(db, id=email_address.id)

@router.delete("/customers/mobile_number")
def delete_mobile_address(mobile_number: MobileNumberDelete, db: Session = Depends(get_db)):
    return mobile_number_crud.remove(db, id=mobile_number.id)

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
    return bussiness_crud.get(db, id=id)

# Get All Customers Business
@router.get("/customers/business/{offset}/{limit}", response_model=BusinessList)
def get_all_businesses(offset: int, limit: int, db: Session = Depends(get_db)):
    return BusinessList(customers=bussiness_crud.get_multi(db, offset=offset, limit=limit), count=bussiness_crud.get_count(db=db))

# Update Business
@router.put("/customers/business")
def update_business(business: BussinessUpdate, db: Session = Depends(get_db)):
    business_obj = bussiness_crud.get(db, id=business.id)
    return bussiness_crud.update(db, db_obj=business_obj, update_schema=business
                                 )

# Delete Customer Individual
# Delete Customer Business


# Utils
@router.get("/customers/business-types")
def get_business_types():
    business_types = [
        {"key": bt.value, "value": get_business_type_string(bt.value)}
        for bt in BusinessType
    ]
    return {"data": business_types}


@router.get("/customers/marital-status")
def get_marital_status():
    marital_status = [
        {"key": bt.value, "value": get_marital_status_string(bt.value)}
        for bt in MaritalStatus
    ]
    return {"data": marital_status}


@router.get("/customers/occupation-status")
def get_occupation_status():
    occupation_status = [
        {"key": bt.value, "value": get_occupation_status_string(bt.value)}
        for bt in OccupationStatus
    ]
    return {"data": occupation_status}


@router.get("/customers/gender-options")
def get_gender_options():
    gender_options = [
        {"key": bt.value, "value": get_gender_string(bt.value)}
        for bt in Gender
    ]
    return {"data": gender_options}
