import sys
from typing import Dict, Any
def get_tracback() -> Dict[str, Any]:
    exc_type, exc_value, exc_tb = sys.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return {
        'error_type': str(exc_type),
        'line_number': line_number,
        'filename': filename,
    }