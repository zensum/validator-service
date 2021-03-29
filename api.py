from typing import Optional, Tuple, Dict, Any
from functools import wraps

from flask import jsonify, request

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
def validate() -> Tuple[bool, str, Optional[Any]]:
    payload = request.json

    country_code: Optional[str] = payload.get('country_code')

    phone_number: Optional[str] = payload.get('phone_number')
    email: Optional[str] = payload.get('email')
    account: Optional[Dict] = payload.get('account')

    if not any([phone_number, email, account]):
        return False, 'Need account, email or phone number', None
    elif sum([1 for x in [email, phone_number, account] if x]) > 1:
        return False, 'Can only take one prop!', None

    if phone_number:
        return validators.phone_number.validate(phone_number)
    elif email:
        return validators.email.validate(email)
    elif account:
        if not country_code:
            return False, 'Need country_code to validate account', account
        return validators.account.validate(account, country_code)
    return False, '', None  # should never reach this!
