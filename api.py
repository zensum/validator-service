from typing import Optional, Tuple
from functools import wraps

from flask import jsonify

import validators.phone_number
import validators.email


def responder(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        valid, message, formatted = func(*args, **kwargs)
        resp = dict(valid=valid, formatted=formatted)
        if not valid:
            resp.update(dict(message=message))
        return jsonify(resp), 200 if valid else 400
    return wrapper


@responder
def validate(phone_number: Optional[str] = None, email: Optional[str] = None) -> Tuple[bool, str]:
    if not any([phone_number, email]):
        return False, 'Need email or phone number', None
    elif all([phone_number, email]):
        return False, 'Can only take either phone number or email', None

    if phone_number:
        return validators.phone_number.validate(phone_number)
    elif email:
        return validators.email.validate(email)
