from typing import Tuple
from email_validator import validate_email  # type: ignore


def validate(email: str) -> Tuple[bool, str, str]:
    try:
        validate_email(email)
        return True, '', email
    except Exception:
        return False, 'Not a valid email', email
