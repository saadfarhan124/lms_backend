from sqlalchemy.orm import Session

from app.models import Customer, Individual, Employer, Address, MobileNumber, EmailAddress, Business
from app.schemas import CustomerCreate, CustomerUpdate, EmployerCreate, EmployerUpdate, EmailAddressCreate, EmailAddressUpdate, AddressCreate, AddressUpdate, MobileNumberCreate, MobileNumberUpdate, IndividualUpdate, IndividualCreate, BussinessCreate, BussinessUpdate
from app.utils.base import CRUDBase


class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
    pass


class CRUDEmployer(CRUDBase[Employer, EmployerCreate, EmployerUpdate]):
    pass

class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    pass

class CRUDEmailAddress(CRUDBase[EmailAddress, EmailAddressCreate, EmailAddressUpdate]):
    pass

class CRUDMobileNumbers(CRUDBase[MobileNumber, MobileNumberCreate, MobileNumberUpdate]):
    pass

class CRUDIndividuals(CRUDBase[Individual, IndividualCreate, IndividualUpdate]):
    pass

class CRUDBussiness(CRUDBase[Business, BussinessCreate, BussinessUpdate]):
    pass

customer = CRUDCustomer(Customer)
employer_crud = CRUDEmployer(Employer)
address_crud = CRUDEmployer(Address)
email_address_crud = CRUDEmailAddress(EmailAddress)
mobile_number_crud = CRUDMobileNumbers(MobileNumber)
individual_crud = CRUDIndividuals(Individual)
bussiness_crud = CRUDBussiness(Business)