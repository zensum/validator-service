import re
import logging
from typing import Literal, NoReturn, Optional, Union
from functools import cache

import phonenumbers  # type: ignore

from config import Config


def _exception() -> NoReturn:
    raise ValueError('Not a valid phone number for any of the supported countries.')


def _validate_and_normalize(p: str, cc: str = None, _try_again: bool = True) -> str:
    # cc needs to be SE or NO
    try:
        p = re.sub(r'[^0-9+]', '', p)
        if p.startswith('00'):
            p = '+' + p[2:]
        p = phonenumbers.parse(p, cc)
        if not phonenumbers.is_valid_number(p):
            raise Exception()
        return str(phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164))
    except Exception as e:
        if _try_again:
            return _validate_and_normalize(f'+{p}', cc, _try_again=False)
        else:
            raise e


@cache
def validate_and_normalize(phone_number: str, country_code: Optional[str] = None) -> str:
    try:
        if country_code:
            return _validate_and_normalize(phone_number, country_code)
        else:
            logging.warning('Validating phone_number without knowing country!')

            def safe_validator(p: str, cc: str) -> Union[str, Literal[False]]:
                try:
                    return validate_and_normalize(p, cc)
                except Exception:
                    return False
            p = next(safe_validator(phone_number, cc) for cc in Config.countries)
            if not p:
                raise _exception()
            return p
    except Exception:
        return _exception()
