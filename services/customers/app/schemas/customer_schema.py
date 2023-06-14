from pydantic import BaseModel, validator
from typing import Union
from datetime import date
from app.constants import get_marital_status_string, get_business_type_string, get_gender_string, get_occupation_status_string

class EmployerCreate(BaseModel):
    name: str
    address: str
    email: str
    number: str
    individual_id: Union[int, None]


class EmployerUpdate(BaseModel):
    pass

class Employer(EmployerCreate):
    id:int
    class Config:
        orm_mode = True


class AddressCreate(BaseModel):
    street: str
    village: str
    district: str
    nearest_landmark: str
    country: str
    individual_id: Union[int, None]


class AddressUpdate(BaseModel):
    pass

class Address(AddressCreate):
    id: int
    class Config:
        orm_mode = True

class MobileNumberCreate(BaseModel):
    number: str
    individual_id: Union[int, None]


class MobileNumberUpdate(BaseModel):
    pass


class MobileNumber(MobileNumberCreate):
    id: int
    class Config:
        orm_mode = True


class EmailAddressCreate(BaseModel):
    email: str
    individual_id: Union[int, None]

class EmailAddressUpdate(BaseModel):
    pass

class EmailAddress(EmailAddressCreate):
    id: int
    class Config:
        orm_mode = True


class IndividualCreate(BaseModel):
    customer_id: Union[int, None]
    first_name: str
    last_name: str
    middle_name: Union[str, None]
    date_of_birth: date
    citizenship: str
    marrital_status: int
    occupation_status: int
    gender: int
    employer: EmployerCreate
    address: AddressCreate
    email_addresses: list[EmailAddressCreate]

    @validator("email_addresses")
    def validate_email_addresses(cls, email_addresses, values, **kwargs):
        if len(email_addresses) < 1:
            raise ValueError(
                "List of email addresses must have at least one item")
        return email_addresses

    mobile_numbers: list[MobileNumberCreate]

    @validator("mobile_numbers")
    def validate_mobile_numbers(cls, mobile_numbers, values, **kwargs):
        if len(mobile_numbers) < 1:
            raise ValueError(
                "List of mobile numbers must have at least one item")
        return mobile_numbers


class IndividualUpdate(BaseModel):
    pass



class CustomerCreate(BaseModel):
    photo: str
    user_type: int
    individual: IndividualCreate
    # individual: Union[IndividualCreate, None]


class CustomerUpdate(BaseModel):
    id: int

class Customer(BaseModel):
    id: int
    photo: str
    user_type: int
    
    class Config:
        orm_mode = True

class Individual(IndividualCreate): 
    id:int
    employer: Employer
    address: Address
    email_addresses: list[EmailAddress]
    mobile_numbers: list[MobileNumber]
    customer: Customer
    marrital_status_string: str = None
    occupation_status_str: str = None
    gender_str: str = None

    @validator("marrital_status_string", always=True)
    def marital_status_string(cls, v, values, **kwargs):
        return f"{get_marital_status_string(values['marrital_status'])}"
    
    @validator("occupation_status_str", always=True)
    def occupation_status_string(cls, v, values, **kwargs):
        return f"{get_occupation_status_string(values['occupation_status'])}"

    @validator("gender_str", always=True)
    def gender_string(cls, v, values, **kwargs):
        return f"{get_gender_string(values['gender'])}"
    
    class Config:
        orm_mode = True

