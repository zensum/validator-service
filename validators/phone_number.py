import os
import re
from typing import Tuple

import phonenumbers  # type: ignore

SUPPORTED_COUNTRIES = list(map(lambda x: x.strip().upper(), os.getenv('SUPPORTED_COUNTRIES', 'SE,NO').split(',')))


def _validate(p: str, cc: str = None, _try_again=True) -> Tuple[bool, str, str]:
    try:
        p = re.sub(r'[^0-9+]', '', p)
        if p.startswith('00'):
            p = '+' + p[2:]
        p = phonenumbers.parse(p, cc)
        if not phonenumbers.is_valid_number(p):
            raise Exception()
        return True, '', str(phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164))
    except Exception:
        if _try_again:
            return _validate(f'+{p}', cc, _try_again=False)
    return False, f'Not a valid phone number for {cc}', p


def validate(phone_number: str) -> Tuple[bool, str, str]:
    for c in [None, *list(SUPPORTED_COUNTRIES)]:
        valid, message, p = _validate(phone_number, c)
        if valid:
            return valid, message, p
    return False, 'Not valid phone number for any of the supported countries', phone_number
