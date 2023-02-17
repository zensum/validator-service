import json
import logging
import time
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import ClientDisconnect
from starlette.responses import Response

from config import Config
from routers.middlewares.request_id import RequestIDContextMiddleware
from routers.validator import router as validator_router
from routers.validator import router_v2 as validator_router_v2
from utils.setup_logger import setup_logging

app: FastAPI = FastAPI(
    title='The Validator by Zensum',
    description=f"""
A __Validator service__ built at Zensum.

---
### Code

You can find this code [here on Github](https://github.com/zensum/validator-service).

---

### Features
 - Validating for Sweden and Norway
  - emails
  - phone numbers
  - account numbers
  - personal ids

---

### Request ID
Please add a value to the header `{Config.request_id_key}` with a UUID4 value to be able to track
the request between servies. 🙏🏼

---

### Support
Pray 🙏🏼

---
""",
    openapi_tags=[
        {
            'name': 'Validator',
            'description': '__Validating__. This method validates emails, phone numbers, pni and accounts. '
        },
    ],
)

if Config.REQUIRE_HTTPS:
    from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

    app.add_middleware(HTTPSRedirectMiddleware)


@app.on_event('startup')
async def startup_event() -> None:
    setup_logging()
    # noinspection PyStatementEffect
    # Checks that all necessary envs are set with an overkill map
    *map(lambda k: k.startswith('__') or getattr(Config, k), dir(Config.__class__)),


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):  # type: ignore
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(round(process_time * 1000)) + ' ms'
    if response.headers.get('server'):
        del response.headers['server']
    return response


app.add_middleware(RequestIDContextMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.Origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=[Config.request_id_key, 'Content-Type'],
)


@app.middleware('http')
async def add_cache_header(request: Request, call_next):  # type: ignore
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(round(process_time * 1000)) + ' ms'

    response.headers['Cache-Control'] = f'max-age={10*60}'  # 10 min

    return response


app.include_router(
    validator_router,
    tags=['Validator'],
)


app.include_router(
    validator_router_v2,
    prefix='/v2',
    tags=['Validator'],
)


async def http_exception_middleware(request: Request, call_next: Any) -> Response:
    try:
        resp = await call_next(request)
        if request.url.path.startswith('/v2') and resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            return Response(
                json.dumps({'valid': False}),
                status_code=status.HTTP_200_OK,
                headers={
                    header: resp.headers[header]
                    for header in resp.headers
                    if header != 'content-length'
                },
            )
        return resp
    except ClientDisconnect:
        return Response(status_code=499)
    except HTTPException as e:
        return Response(json.dumps(dict(detail=e.detail)), status_code=e.status_code, headers=e.headers)
    except Exception as e:
        logging.info(f'Exception: {e}', exc_info=e)
        return Response(json.dumps(dict(detail=str(e))), status_code=500)

# this must be last middleware registered to catch all HTTPException exceptions in middlewares and convert to response
app.add_middleware(BaseHTTPMiddleware, dispatch=http_exception_middleware)
