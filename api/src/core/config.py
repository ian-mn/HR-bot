import os
from functools import lru_cache
from logging import config as logging_config

from core.logger import LOGGING
from pydantic_settings import BaseSettings

logging_config.dictConfig(LOGGING)


class Config(BaseSettings):
    project_name: str

    redis_host: str
    redis_port: int

    logging_level: str

    code_expiration_secs: int
    auth_expiration_secs: int

    sms_api_key: str
    sms_api_email: str


@lru_cache()
def get_config() -> Config:
    return Config()
