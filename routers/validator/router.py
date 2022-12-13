from typing import Any, Dict, Type, Union

from fastapi import APIRouter

from .payload import PNI, BankAccount, Email, PhoneNumber, ResponseModel

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


@router.post('/safe', response_model=ResponseModel)
async def validate_safely(
    body: Dict[str, Any],
) -> ResponseModel:
    models: list[Type[Union[Email, PNI, PhoneNumber, BankAccount]]] = [Email, PNI, PhoneNumber, BankAccount]
    for m in models:
        try:
            parsed_model: Union[Email, PNI, PhoneNumber, BankAccount] = m.parse_obj(body)
            for k in parsed_model.dict():
                if k not in ['country']:
                    return ResponseModel(
                        formatted=getattr(parsed_model, k),
                        valid=True,
                    )
        except Exception:
            pass
    return ResponseModel(
        formatted=None,
        valid=False,
    )
