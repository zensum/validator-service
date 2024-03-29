from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, validator

from config import Config
from validator import account, email, phone_number, pni


class Country(BaseModel):
    country: Optional[str] = Field(example='SE')

    @validator('country', check_fields=False)
    def validate_country(cls, value: str) -> str:
        if value and value not in Config.countries:
            raise ValueError(f'{value} is not in {",".join(Config.countries)}')
        return value


class BankAccount(BaseModel):
    clearing_number: Optional[str] = Field(example='1337')
    account_number: str = Field(..., example='1234567')


class PNI(Country):
    pni: str = Field(..., example='194907011813')

    @validator('pni')
    def validate_pni(cls, value: str, values: Dict[str, Any]) -> str:
        return pni.validate_and_normalize(value, values.get('country'))


class Email(Country):
    email: EmailStr

    @validator('email')
    def validate_email(cls, value: str) -> str:
        email.is_email(value)
        return value


class PhoneNumber(Country):
    phone_number: str = Field(..., example='+46761234567')

    @validator('phone_number')
    def validate_phone_number(cls, value: str, values: Dict[str, Any]) -> str:
        return phone_number.validate_and_normalize(value, values.get('country'))


class Account(Country):
    account: Optional[BankAccount] = None

    @validator('account')
    def validate_account(cls, value: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
        return account.validate(value, values.get('country'))


class ResponseModel(BaseModel):
    valid: bool = Field(..., example=True)
    formatted: Any
