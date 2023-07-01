from app.models import Guarantor, LoanApplication, LoanApplicationCheques, LoanApplicationPaymentSchedule
from app.models import Guarantor, Fees, PreDefinedFees
from app.schemas import GuarantorCreate, GuarantorUpdate
from app.schemas import LoanApplicationCreate, LoanApplicationUpdate
from app.schemas import LoanApplicationPaymentScheduleCreate, LoanApplicationPaymentScheduleUpdate
from app.schemas import LoanApplicationChequesCreate, LoanApplicationChequesUpdate
from app.schemas import FeesCreate, FeesUpdate
from app.schemas import PreDefinedFeesCreate, PreDefinedFeesUpdate
from app.utils.base import CRUDBase

class CRUDLoanApplication(CRUDBase[LoanApplication, LoanApplicationCreate, LoanApplicationUpdate]):
    pass

class CRUDGuarantor(CRUDBase[Guarantor, GuarantorCreate, GuarantorUpdate]):
    pass

class CRUDLoanApplicationPaymentSchedule(CRUDBase[LoanApplicationPaymentSchedule, LoanApplicationPaymentScheduleCreate, LoanApplicationPaymentScheduleUpdate]):
    pass

class CRUDLoanApplicationCheques(CRUDBase[LoanApplicationCheques, LoanApplicationChequesCreate, LoanApplicationChequesUpdate]):
    pass

class CRUDFees(CRUDBase[Fees, FeesCreate, FeesUpdate]):
    pass

class CRUDPreDefinedFees(CRUDBase[PreDefinedFees, PreDefinedFeesCreate, PreDefinedFeesUpdate]):
    pass

loan_application_crud = CRUDLoanApplication(LoanApplication)
guarantor_crud = CRUDGuarantor(Guarantor)
loan_application_payment_schedule_crud = CRUDLoanApplicationPaymentSchedule(LoanApplicationPaymentSchedule)
loan_application_cheques_crud = CRUDLoanApplicationCheques(LoanApplicationCheques)
fees_crud = CRUDFees(Fees)
predefined_fees_crud = CRUDPreDefinedFees(PreDefinedFees)

