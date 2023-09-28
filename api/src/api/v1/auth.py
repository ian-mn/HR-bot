from http import HTTPStatus

from fastapi import APIRouter, Depends
from models.models import BoolResponse, PhoneReponse
from services.auth_service import AuthService, get_auth_service

router = APIRouter()


@router.get(
    "/is_authorized/{user_id}",
    response_model=PhoneReponse,
    summary="Is user authorized?",
)
async def is_authorized(
    user_id: str,
    service: AuthService = Depends(get_auth_service),
) -> PhoneReponse:
    result = await service.is_authorized(user_id)
    return PhoneReponse(result=result)


@router.post(
    "/send_verification_code/",
    summary="Send code via sms",
)
async def send_verification_code(
    phone: str,
    user_id: str,
    service: AuthService = Depends(get_auth_service),
) -> None:
    await service.send_verification_code(phone, user_id)


@router.get(
    "/verify_code/",
    summary="Verify code",
    response_model=BoolResponse,
)
async def verify_code(
    user_id: str,
    user_code: str,
    service: AuthService = Depends(get_auth_service),
) -> BoolResponse:
    result = await service.verify_code(user_id, user_code)
    return BoolResponse(result=result)
