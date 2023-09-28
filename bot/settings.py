from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    support_email: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
