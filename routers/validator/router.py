from typing import Any, Dict, Optional, Union

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
    for m in [Email, PNI, PhoneNumber, BankAccount]:
        try:
            parsed_model = m.parse_obj(body)
            for k in parsed_model.dict():
                if k not in ['country']:
                    return ResponseModel(
                        formatted=body[k],
                        valid=True,
                    )
        except Exception:
            pass
    return ResponseModel(
        formatted=None,
        valid=False,
    )
