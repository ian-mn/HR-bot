import requests


def is_employee(phone: str) -> bool:
    return True


def is_authorized(user_id: str) -> bool:
    with requests.get(f"http://api:8010/api/v1/auth/is_authorized/{user_id}") as r:
        return r.json()["result"]


def send_verification_code(phone: str, user_id: str) -> None:
    requests.post(
        "http://api:8010/api/v1/auth/send_verification_code",
        params={
            "user_id": user_id,
            "phone": phone,
        },
    )


def verify_code(user_id: str, code: str) -> bool:
    with requests.get(
        f"http://api:8010/api/v1/auth/verify_code",
        params={
            "user_id": user_id,
            "user_code": code,
        },
    ) as r:
        return r.json()["result"]


def get_vmi_number(user_id: str) -> str:
    return "3516022-690/22"


def get_salary_days(user_id: str) -> tuple[int, int]:
    return (7, 22)


def get_vacation_days(user_id: str) -> int:
    return 14
