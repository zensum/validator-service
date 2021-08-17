import os
from typing import Dict, Optional, List, Union


class ConfigException(ValueError):
    pass


class _Config(type):
    _envs: Dict[str, Optional[str]] = dict()

    def is_true(self, env: str) -> bool:
        try:
            return self.get_env(env).upper() in ['1', 'TRUE']
        except Exception:
            return False

    def get_env(self, env: str, default: Optional[str] = None) -> str:
        try:
            value = self._envs.get(env) or os.environ[env]
            value = value.strip('"')
            self._envs[env] = value
            return value
        except KeyError:
            if default is not None:
                return default
            raise ConfigException(env)

    @property
    def APP_ENV(self) -> str:
        accepted_values = ['PRODUCTION', 'DEVELOPMENT', 'STAGING', 'LOCAL']
        a = os.getenv('APP_ENV')
        if not a:
            raise ConfigException('APP_ENV')
        elif a not in ['PRODUCTION', 'DEVELOPMENT', 'STAGING', 'LOCAL']:
            raise ConfigException(f'{a} is not a valid valur for APP_ENV, can only be {", ".join(accepted_values)}')
        return os.environ['APP_ENV']

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == 'PRODUCTION'

    @property
    def FORCE_SSL(self) -> bool:
        return self.is_true('FORCE_SSL') or self.is_production

    @property
    def REQUIRE_HTTPS(self) -> bool:
        return self.is_true('REQUIRE_HTTPS')

    @property
    def is_web_worker(self) -> bool:
        return self.is_true('WEB_WORKER')

    @property
    def Origins(self) -> List[str]:
        env_origins = os.getenv('CORS_ORIGINS', '').split(',')
        return [o.strip() for o in env_origins if o] or ['*']

    @property
    def request_id_key(self) -> str:
        return 'X-Request-ID'

    @property
    def LOG_LEVEL(self) -> str:
        return os.getenv('LOG_LEVEL', 'INFO')

    @property
    def VSCODE_DEBUGGING(self) -> bool:
        return self.is_true('VSCODE_DEBUGGING')

    @property
    def countries(self) -> List[str]:
        return ['SE', 'NO']


class Config(metaclass=_Config):
    pass
