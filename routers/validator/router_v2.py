from fastapi import APIRouter

from .payload_v2 import PayloadV2, ResponseModel

router_v2 = APIRouter()


@router_v2.post('/', response_model=ResponseModel)
async def validate_safely(
    body: PayloadV2,
) -> ResponseModel:
    try:
        if isinstance(body, dict):
            body = PayloadV2.parse_obj(body)
        return ResponseModel(
            value=body.__root__.value,
            valid=True,
        )
    except Exception:
        return ResponseModel(
            value=body['value'] if isinstance(body, dict) else body.__root__.value,
            valid=False,
        )
