from enum import Enum


class TermModes(Enum):
    # DAYS = 1
    WEEKS = 2
    MONTHS = 3
    FORTNIGHTLY = 4


def get_term_modes_string(term_mode: int) -> str:
    # if term_mode == TermModes.DAYS.value:
    #     return "Days"
    if term_mode == TermModes.WEEKS.value:
        return "Weeks"
    elif term_mode == TermModes.MONTHS.value:
        return "Months"
    elif term_mode == TermModes.FORTNIGHTLY.value:
        return "Fortnightly"
    return "unknown"


def get_term_type_enum(term_mode: str) -> TermModes:
    # if term_mode.lower() == "days":
    #     return TermModes.DAYS
    if term_mode.lower() == "weeks":
        return TermModes.WEEKS
    elif term_mode.lower() == "months":
        return TermModes.MONTHS
    elif term_mode.lower() == "fortnightly":
        return TermModes.FORTNIGHTLY
    raise ValueError("Invalid Business type string")


def is_valid_term_mode(term_mode: int) -> bool:
    return any(term_mode == mode.value for mode in TermModes)
