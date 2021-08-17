from typing import Any, Dict, Optional, Tuple, Union
import re
import logging

import bankkonto  # type: ignore
from bankkonto import BankkontoValidationError   # type: ignore

from config import Config

def _exception(m: str) -> ValueError:
    return ValueError(f'Not a valid bank account. {m}')


def validate(account: Dict[str, Any], country_code: Optional[str] = None) -> Dict[str, Any]:
    for c in ([country_code] if country_code else Config.countries):
        try:
            return validate_and_normalize(account, c)
        except Exception:
            pass
    raise _exception('Something went wrong')


def validate_and_normalize(account: Dict[str, Any], country_code: str) -> Dict[str, Any]:
    if not country_code or country_code not in ['SE', 'NO']:
        raise _exception('Missing country_code')
    try:
        account_no = account['account_number']
        clearing_no: Optional[str] = account.get('clearing_number')
        bank_id: int = account['bank_id']
        bank_name: str = account['bank_name']
        if not bank_id or type(bank_id) is not int:
            raise _exception('bank_id is not int')
        if not bank_name or type(bank_name) is not str:
            raise _exception('bank_name is not str')
        if not account_no:
            raise _exception('Missing account_number')

        if country_code == 'SE':
            if not clearing_no:
                raise _exception('Missing clearing_number')
            clearing_no, account_no = format_bank_account_se(clearing_no, account_no)
            try:
                bankkonto.validate(clearing_no, account_no)
            except bankkonto.exceptions.SwedbankBankkontoValidationError:
                if len(account_no) == 10:
                    raise _exception('invalid control digit for Swedbank account - please double check.')
                raise _exception('invalid account length for Swedbank account')
            except (bankkonto.exceptions.BankkontoValidationError, BankkontoValidationError) as e:
                raise _exception(str(e))
            except Exception:
                raise _exception('Account validation error')

        elif country_code == 'NO':
            if clearing_no:
                raise _exception('Clearing number is not supported in NO')
            clearing_no = None
            account_no = format_bank_account_no(account_no)
            if len(account_no) != 11:
                raise _exception(f'Required length of account number in NO is 11 digits not {len(account_no)}')
        else:
            raise _exception('Not a supported country for account validation.')
    except ValueError as e:
        raise e
    except Exception as e:
        raise _exception(str(e))

    return {
        'bank_id': bank_id,
        'bank_name': bank_name,
        'clearing_number': clearing_no,
        'account_number': account_no,
    }


def format_bank_account_no(account_no: str) -> str:
    return purge_non_digits(account_no)


def format_bank_account_se(clearing_no: str, account_no: str) -> Tuple[str, str]:
    """
        Removes non-digit characters from clearing and account.
        If 5th digit of clearing is already moved to account part it moves it to clearing for validation.
        Fills Swedbank account with zeroes up to expected length.
    """
    clearing_no = purge_non_digits(clearing_no)
    account_no = purge_non_digits(account_no)

    # for Swedbank, sigh
    if len(clearing_no) == 4 and clearing_no[0] == '8':
        swedbank_account_length = bankkonto.account.expected_account_length(clearing_no + account_no[0])
        if len(account_no) >= swedbank_account_length + 1:
            clearing_no += account_no[0]  # add 5th digit temporarily for validation
            account_no = account_no[1:]
            if len(account_no) != swedbank_account_length:
                logging.warning('Swedbank account number has too many digits')
        else:
            clearing_no += '0'
            logging.warning('Not enough digits for Swedbank clearing or account number. Added 0 to clearing.')
    if clearing_no and bankkonto.account.is_swedbank(clearing_no):
        account_no = account_no.zfill(bankkonto.account.expected_account_length(clearing_no))

    return move_swedbank_digit(clearing_no, account_no)


def truncate_swedbank_clearing_number(clearing_no: str, account_no: str) -> Tuple[str, str]:
    """Truncates clearing number to 4 digits for Swedbank which clearing numbers starting with 8 may have 5 digits"""
    if clearing_no[:1] == '8' and len(clearing_no) > 4:  # for Swedbank
        clearing_no = clearing_no[:4]
    return clearing_no, account_no


def move_swedbank_digit(clearing_no: str, account_no: str) -> Tuple[str, str]:
    """Moves last digit of 5-digit clearing number starting with 8 to front of account part"""
    if clearing_no[:1] == '8' and len(clearing_no) > 4:  # for Swedbank
        account_no = clearing_no[4] + account_no
    clearing_no, account_no = truncate_swedbank_clearing_number(clearing_no=clearing_no, account_no=account_no)
    return clearing_no, account_no


def purge_non_digits(text: str) -> str:
    return re.sub(r'[^0-9]', '', text)  # remove unwanted characters
