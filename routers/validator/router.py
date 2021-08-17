from typing import Union

from fastapi import APIRouter

from .payload import ResponseModel, PNI, Email, PhoneNumber, BankAccount


router = APIRouter()


@router.post('/', response_model=ResponseModel)
async def validate(
    body: Union[Email, PNI, PhoneNumber, BankAccount],
) -> ResponseModel:
    for k in body.dict():
        if k not in ['country']:
            return ResponseModel(
                formatted=getattr(body, k),
                valid=True,
            )
    raise ValueError('Could not figure out what to return')
