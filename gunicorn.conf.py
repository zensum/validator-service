import os

_w = int(os.getenv('GUNICORN_WORKERS', '6'))

workers = _w
worker_connections = 1000
timeout = 30
keepalive = int(_w / 2)
