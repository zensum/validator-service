from typing import Dict

from config import Config
from utils.request_id import get_request_id


def get_headers(token: str | None = None) -> Dict[str, str]:
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    request_id = get_request_id()
    if request_id:
        headers[Config.request_id_key] = request_id
    return headers
