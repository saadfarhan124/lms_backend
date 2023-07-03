import sys
from typing import Dict, Any
from app.constants import get_loan_status_string, get_loan_type_string


def get_tracback() -> Dict[str, Any]:
    exc_type, exc_value, exc_tb = sys.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return {
        'error_type': str(exc_type),
        'line_number': line_number,
        'filename': filename,
    }

def get_formatted_date(date):
    # Assuming the date_of_birth value is a string
    # Determine the day suffix
    if date.day in (1, 21, 31):
        suffix = "st"
    elif date.day in (2, 22):
        suffix = "nd"
    elif date.day in (3, 23):
        suffix = "rd"
    else:
        suffix = "th"
    formatted_date = date.strftime(f"%d{suffix} %b, %Y")
    return f"{formatted_date}"
