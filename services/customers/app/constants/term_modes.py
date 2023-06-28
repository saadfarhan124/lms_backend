from enum import Enum

class TermModes(Enum):
    DAYS = 1
    WEEKS = 2
    MONTHS = 3

def get_term_modes_string(term_mode: int) -> str:
    if term_mode == TermModes.DAYS.value:
        return "Days"
    elif term_mode == TermModes.WEEKS.value:
        return "Weeks"
    elif term_mode == TermModes.MONTHS.value:
        return "Months"
    return "unknown"

def get_term_type_enum(term_mode: str) -> TermModes:
    if term_mode.lower() == "days":
        return TermModes.DAYS
    elif term_mode.lower() == "weeks":
        return TermModes.WEEKS
    elif term_mode.lower() == "months":
        return TermModes.MONTHS
    raise ValueError("Invalid Business type string")