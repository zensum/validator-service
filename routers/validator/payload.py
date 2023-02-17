from typing import Any, Dict

from pydantic import BaseModel, EmailStr, Field, validator

from shared.common import Country
from shared.validator import email, phone_number, pni
from validator import account


class CountryModel(BaseModel):
    country: Country | None = Field(example=Country.SWEDEN.value)


class BankAccount(BaseModel):
    clearing_number: str | None = Field(example='1337')
    account_number: str = Field(..., example='1234567')


class PNI(CountryModel):
    pni: str = Field(..., example='194907011813')

    @validator('pni')
    def validate_pni(cls, value: str, values: Dict[str, Any]) -> str:
        return pni.validate_and_normalize(value, values.get('country'))


class Email(CountryModel):
    email: EmailStr

    @validator('email')
    def validate_email(cls, value: str) -> str:
        email.is_email(value)
        return value


class PhoneNumber(CountryModel):
    phone_number: str = Field(..., example='+46761234567')

    @validator('phone_number')
    def validate_phone_number(cls, value: str, values: Dict[str, Any]) -> str:
        return phone_number.validate_and_normalize(value, values.get('country'))


class Account(CountryModel):
    account: BankAccount | None

    @validator('account')
    def validate_account(cls, value: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
        return account.validate(value, values.get('country'))


class ResponseModel(BaseModel):
    valid: bool = Field(..., example=True)
    formatted: Any
