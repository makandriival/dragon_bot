import re
from datetime import datetime

DATE_FORMAT = "%d.%m.%Y"

from package.bot_exceptions import InvalidDateError, InvalidEmailError, InvalidPhoneNumberError

def validate_email(email: str) -> None:
    if not email:
        return
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise InvalidEmailError(f"Invalid email: {email}")

def validate_phone(phone: str) -> None:
    cleaned = re.sub(r"[^0-9]", "", phone)
    if len(cleaned) < 7 or len(cleaned) > 15:
        raise InvalidPhoneNumberError(f"Invalid phone number: {phone}")

def validate_birthday(birthday: str) -> str:
    if not birthday:
        return ""
    try:
        datetime.strptime(birthday, DATE_FORMAT)
        return birthday
    except ValueError:
        raise InvalidDateError(f"Birthday must be in format {DATE_FORMAT}.")