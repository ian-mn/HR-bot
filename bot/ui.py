from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from settings import settings


def get_greeting(full_name: str) -> str:
    return f"""Здравствуйте, {full_name}! 
Выберите интересующий Вас раздел:"""


dms_btn = InlineKeyboardButton(
    text="ДМС",
    callback_data="vmi",
)
salary_btn = InlineKeyboardButton(
    text="Дни выплаты зарплаты",
    callback_data="salary_days",
)
vacation_btn = InlineKeyboardButton(
    text="Дни отпуска",
    callback_data="vacation_days",
)
info_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
        [
            [dms_btn],
            [salary_btn],
            [vacation_btn],
        ]
)


share_contact_msg = "Поделитесь своим номером телефона:"

share_contact_btn = KeyboardButton(
    text="Отправить номер телефона 📱",
    request_contact=True,
)
contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[[share_contact_btn]],
    resize_keyboard=True,
)

verification_code_sent_msg = "В течение минуты Вам будет направлено смс с кодом доступа. Пожалуйста, введите код ниже:"


not_employee_msg = f"""К сожалению, у Вас нет доступа. Пожалуйста, обратитесь к администратору {settings.support_email}. 
В заявке укажите Ваше ФИО, Департамент и актуальный номер телефона."""

incorrect_verification_code_msg = "Некорректный код подтверждения."


def get_vmi_msg(vmi_number: str) -> str:
    return f"""Номер полиса ДМС: {vmi_number}
Записаться на прием к врачу:
- по телефону +7(495)956-11-66 или +7(800)234-57-37 
- по почте doctor@reso.ru
- в приложении РЕСО Мобайл (для iOS и Android)
Получить консультацию у врача-куратора Сироткина Максима по телефону +7(495)730-30-00 доб. 2194 или по почте sirmm@reso.ru
"""


def get_salary_days_msg(first_day: int, second_day: int) -> str:
    return f"""Аванс - {first_day} числа;
Задаток - {second_day} числа.
"""


def get_vacation_days_msg(vacation_days: int) -> str:
    if vacation_days:
        return f"Накоплено дней отпуска: {vacation_days}"
    return "Все дни отпуска потрачены."
