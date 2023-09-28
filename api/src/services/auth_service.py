import random
import string
from functools import lru_cache

from core.config import get_config
from db.auth_storage import AbstractAuthStorage, get_auth_storage
from fastapi import Depends
from smsaero import SmsAero


class AuthService:
    def __init__(self, auth_db: AbstractAuthStorage):
        self.auth_db = auth_db

    async def is_authorized(self, user_id) -> bool:
        phone = await self.auth_db.get(f"auth_{user_id}")
        return phone

    async def send_verification_code(self, phone: str, user_id: str) -> None:
        code = "".join(random.choices(string.digits, k=4))

        sms_api = SmsAero(
            get_config().sms_api_email,
            get_config().sms_api_key,
        )
        sms_api.send(phone, f"Код подтверждения: {code}")

        await self.auth_db.set(f"code_{user_id}", f"{phone}_{code}")
        await self.auth_db.expire(f"code_{user_id}", get_config().code_expiration_secs)

    async def verify_code(self, user_id: str, user_code: str) -> bool:
        value = await self.auth_db.get(f"code_{user_id}")
        phone = value.split("_")[0]
        code = value.split("_")[1]
        if code == user_code:
            await self.auth_db.set(f"auth_{user_id}", phone)
            await self.auth_db.expire(
                f"auth_{user_id}", get_config().auth_expiration_secs
            )
            return True
        return False


@lru_cache()
def get_auth_service(
    auth_db: AbstractAuthStorage = Depends(get_auth_storage),
) -> AuthService:
    return AuthService(auth_db)
