from uuid import uuid4
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from config import Config
from utils.request_id import set_request_id, get_request_id, reset_request_id


class RequestIDContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id_token = set_request_id(request.headers.get(Config.request_id_key, str(uuid4())))

        try:
            response = await call_next(request)
            response.headers[Config.request_id_key] = get_request_id()
            return response
        except Exception as e:
            raise e
        finally:
            reset_request_id(request_id_token)
