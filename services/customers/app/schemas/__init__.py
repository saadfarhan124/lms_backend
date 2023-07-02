from .customer_schema import Customer, CustomerCreate, CustomerUpdate
from .customer_schema import EmployerCreate, EmployerUpdate
from .customer_schema import AddressCreate, AddressUpdate
from .customer_schema import EmailAddressUpdate, EmailAddressCreate, EmailAddressDelete
from .customer_schema import MobileNumberCreate, MobileNumberUpdate, MobileNumberDelete
from .customer_schema import Individual, IndividualCreate, IndividualUpdate, IndividualList
from .customer_schema import BussinessCreate, BussinessCustomerCreate, BussinessUpdate, Business, BusinessList


from .loan_application_schema import LoanApplicationCreate, LoanApplicationUpdate, LoanApplication
from .loan_application_schema import GuarantorCreate, GuarantorUpdate, Guarantor, GuarantorsList
from .loan_application_schema import LoanApplicationPaymentScheduleCreate, LoanApplicationPaymentScheduleUpdate, LoanApplicationPaymentSchedule
from .loan_application_schema import LoanApplicationChequesCreate, LoanApplicationChequesUpdate, LoanApplicationCheques
from .loan_application_schema import FeesCreate, FeesUpdate, Fees
from .loan_application_schema import PreDefinedFeesCreate, PreDefinedFeesUpdate, PreDefinedFees
from .loan_application_schema import PaymentSchedule