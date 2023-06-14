from enum import Enum

class Gender(Enum):
    Male = 1
    Female = 2
    Other = 3

def get_gender_string(gender: Gender) -> str:
    if gender == Gender.Male.value:
        return "Male"
    elif gender == Gender.Female.value:
        return "Female"
    elif gender == Gender.Other.value:
        return "Other"
    return "unknown"

def get_gender_name(gender: str) -> Gender:
    if gender.lower() == "male":
        return Gender.Male
    elif gender.lower() == "female":
        return Gender.Female
    elif gender.lower() == "other":
        return Gender.Other
    raise ValueError("Invalid Gender Type")