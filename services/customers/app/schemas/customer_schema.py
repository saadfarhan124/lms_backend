from pydantic import BaseModel, validator
from typing import Union, List
from datetime import date, datetime
from app.constants import CustomerType, get_marital_status_string, get_business_type_string, get_gender_string, get_occupation_status_string


class EmployerCreate(BaseModel):
    name: str
    address: str
    email: str
    number: str
    individual_id: Union[int, None]


class EmployerUpdate(EmployerCreate):
    id: int


class Employer(EmployerCreate):
    id: int

    class Config:
        orm_mode = True


class AddressCreate(BaseModel):
    street: str
    village: str
    district: str
    nearest_landmark: str
    country: str
    individual_id: Union[int, None]


class AddressUpdate(AddressCreate):
    id: int


class Address(AddressCreate):
    id: int

    class Config:
        orm_mode = True


class MobileNumberCreate(BaseModel):
    number: str
    individual_id: Union[int, None]


class MobileNumberUpdate(MobileNumberCreate):
    id: Union[int, None]


class MobileNumberDelete(MobileNumberUpdate):
    pass


class MobileNumber(MobileNumberCreate):
    id: int

    class Config:
        orm_mode = True


class EmailAddressCreate(BaseModel):
    email: str
    individual_id: Union[int, None]


class EmailAddressUpdate(EmailAddressCreate):
    id: Union[int, None]

class EmailAddressDelete(EmailAddressUpdate):
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


class IndividualUpdate(IndividualCreate):
    id: int
    employer: Union[EmployerCreate, None]
    address: Union[AddressCreate, None]
    email_addresses: List[EmailAddressUpdate]
    mobile_numbers: List[MobileNumberUpdate]


class CustomerBase(BaseModel):
    photo: str
    user_type: int = CustomerType.INDIVIDUAL.value


class CustomerCreate(CustomerBase):
    individual: IndividualCreate


class CustomerUpdate(BaseModel):
    id: int


class Customer(BaseModel):
    id: int
    photo: str
    user_type: int

    class Config:
        orm_mode = True


class Individual(IndividualCreate):
    id: int
    employer: Employer
    address: Address
    email_addresses: list[EmailAddress]
    mobile_numbers: list[MobileNumber]
    customer: Customer
    marrital_status_string: str = None
    occupation_status_str: str = None
    gender_str: str = None
    formatted_date_str: str = None

    @validator("marrital_status_string", always=True)
    def marital_status_string(cls, v, values, **kwargs):
        return f"{get_marital_status_string(values['marrital_status'])}"

    @validator("occupation_status_str", always=True)
    def occupation_status_string(cls, v, values, **kwargs):
        return f"{get_occupation_status_string(values['occupation_status'])}"

    @validator("gender_str", always=True)
    def gender_string(cls, v, values, **kwargs):
        return f"{get_gender_string(values['gender'])}"

    @validator("formatted_date_str", always=True)
    def get_formatted_date(cls, v, values, **kwargs):
        date_of_birth = values["date_of_birth"]  # Assuming the date_of_birth value is a string
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

class IndividualList(BaseModel):
    customers: List[Individual]
    count: int

class BussinessCreate(BaseModel):
    customer_id: Union[int, None]
    name: str
    business_type: int
    business_number: str
    business_email: str


class BussinessUpdate(BussinessCreate):
    id: int


class BussinessCustomerCreate(CustomerBase):
    user_type: int = CustomerType.BUSINESS.value
    business: BussinessCreate


class Business(BussinessCreate):
    id: int
    customer: Customer
    business_type_str: str = None

    @validator("business_type_str", always=True)
    def business_type_string(cls, v, values, **kwargs):
        return f"{get_business_type_string(values['business_type'])}"

    class Config:
        orm_mode = True


class BusinessList(BaseModel):
    customers: List[Business]
    count: int
