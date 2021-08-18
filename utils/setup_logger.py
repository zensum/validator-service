import logging

from config import Config
from utils.request_id import get_request_id


class RequestIDLogFilter(logging.Filter):
    def filter(self, log_record):  # type: ignore
        log_record.request_id = get_request_id()
        return log_record


def setup_logging() -> None:
    logger = logging.getLogger('root')
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(module)s:%(funcName)s():%(lineno)d | %(request_id)s | %(message)s')
    console_handler = logging.StreamHandler()

    logger.setLevel(Config.LOG_LEVEL)
    console_handler.setLevel(Config.LOG_LEVEL)

    logger.addHandler(console_handler)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIDLogFilter())
