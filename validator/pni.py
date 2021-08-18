import logging
from typing import Optional
from functools import cache

from personnummer.personnummer import Personnummer  # type: ignore
import fodselsnummer  # type: ignore

from config import Config


@cache
def validate_and_normalize(pni: str, country: Optional[str] = None) -> str:
    if not country:
        for cc in Config.countries:
            try:
                return validate_and_normalize(pni, cc)
            except Exception:
                pass
        raise ValueError('Could not validate PNI against any known country')
    elif country == 'SE':
        return Personnummer(pni).format(long_format=True)
    elif country == 'NO':
        if fodselsnummer.check_fnr(pni):
            return pni
        raise ValueError('Unknown error with Norwegian PNI')
    else:
        m = f'Missing validator for {country}. Not validating PNI.'
        logging.warning(m)
        raise ValueError(m)
