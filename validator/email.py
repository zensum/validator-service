from functools import cache

import email_validator  # type: ignore


@cache
def is_email(email: str) -> bool:
    try:
        email_validator.validate_email(email)
        return True
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(str(e))
