from enum import Enum
from typing import Any, Dict, Literal

from pydantic import BaseModel, EmailStr, Field, validator

from shared.common import Country
from shared.validator import email, phone_number, pni


class ValidationType(str, Enum):
    PNI = 'pni'
    EMAIL = 'email'
    PHONE_NUMBER = 'phone_number'


class CommonModel(BaseModel):
    country: Country | None = Field(example=Country.SWEDEN.value)
    type: ValidationType
    value: Any


class PNI(CommonModel):
    value: str = Field(..., example='194907011813')
    type: Literal[ValidationType.PNI]

    @validator('value')
    def validate_pni(cls, value: str, values: Dict[str, Any]) -> str:
        return pni.validate_and_normalize(value, values.get('country'))


class Email(CommonModel):
    value: EmailStr
    type: Literal[ValidationType.EMAIL]

    @validator('value')
    def validate_email(cls, value: str) -> str:
        email.is_email(value)
        return value


class PhoneNumber(CommonModel):
    value: str = Field(..., example='+46761234567')
    type: Literal[ValidationType.PHONE_NUMBER]

    @validator('value')
    def validate_phone_number(cls, value: str, values: Dict[str, Any]) -> str:
        return phone_number.validate_and_normalize(value, values.get('country'))


class PayloadV2(BaseModel):
    __root__: PNI | Email | PhoneNumber = Field(..., discriminator='type', title='PayloadV2')


class ResponseModel(BaseModel):
    valid: bool = Field(..., example=True)
    value: Any
