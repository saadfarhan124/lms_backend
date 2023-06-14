from enum import Enum

class CustomerType(Enum):
    INDIVIDUAL = 1
    BUSINESS = 2

def get_customer_type_string(customer_type: CustomerType) -> str:
    if customer_type == CustomerType.INDIVIDUAL.value:
        return "Individual"
    elif customer_type == CustomerType.BUSINESS.value:
        return "Business"
    else:
        return "Unknown"

def get_customer_type_enum(customer_type_string: str) -> CustomerType:
    if customer_type_string.lower() == "individual":
        return CustomerType.INDIVIDUAL
    elif customer_type_string.lower() == "business":
        return CustomerType.BUSINESS
    else:
        raise ValueError("Invalid customer type string")
    
    