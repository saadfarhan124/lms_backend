from .customer_schema import Customer, CustomerCreate, CustomerUpdate, CustomerReturn
from .customer_schema import EmployerCreate, EmployerUpdate
from .customer_schema import AddressCreate, AddressUpdate
from .customer_schema import EmailAddressUpdate, EmailAddressCreate, EmailAddressDelete
from .customer_schema import MobileNumberCreate, MobileNumberUpdate, MobileNumberDelete
from .customer_schema import Individual, IndividualCreate, IndividualUpdate, IndividualList
from .customer_schema import BussinessCreate, BussinessCustomerCreate, BussinessUpdate, Business, BusinessList


from .loan_application_schema import LoanApplicationList, LoanApplicationCreate, LoanApplicationUpdate, LoanApplication
from .loan_application_schema import GuarantorCreate, GuarantorUpdate, Guarantor, GuarantorsList
from .loan_application_schema import LoanApplicationPaymentScheduleCreate, LoanApplicationPaymentScheduleUpdate, LoanApplicationPaymentSchedule
from .loan_application_schema import LoanApplicationChequesCreate, LoanApplicationChequesUpdate, LoanApplicationCheques
from .loan_application_schema import FeesCreate, FeesUpdate, Fees
from .loan_application_schema import PreDefinedFeesCreate, PreDefinedFeesUpdate, PreDefinedFees
from .loan_application_schema import PaymentSchedule, LoanApplicationWithCustomer, LoanApplicationWithCustomerIndividual, LoanApplicationWithCustomerBusiness
from .loan_application_schema import ScheduleReturn

from .user_schema import UserCreate, UserUpdate, User, UsernameExists, UserList
from .user_schema import Login, LoginResponse, TokenPayload, UpdatePassword
from .user_schema import PermissionsCreate, PermissionsUpdate, UserPermissionsUpdate