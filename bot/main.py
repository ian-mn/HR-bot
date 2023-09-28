import asyncio
import logging
import sys

import ui
import utils
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from settings import settings

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    is_authorized = utils.is_authorized(user_id)

    if not is_authorized:
        await message.answer(
            ui.share_contact_msg,
            reply_markup=ui.contact_keyboard,
        )
    else:
        await message.answer(
            ui.get_greeting(message.from_user.full_name),
            reply_markup=ui.info_keyboard,
        )


@dp.message(F.contact)
async def contact_handler(message: Message) -> None:
    user_id = message.from_user.id
    phone = message.contact.phone_number
    is_employee = utils.is_employee(phone)
    if not is_employee:
        await message.answer(ui.not_employee_msg)
        return
    utils.send_verification_code(phone, user_id)
    await message.answer(
        ui.verification_code_sent_msg, reply_markup=ReplyKeyboardRemove()
    )


@dp.message(F.text)
async def verification_code_handler(message: Message) -> None:
    user_id = message.from_user.id
    input_code = message.text
    is_verified = utils.verify_code(user_id, input_code)
    if not is_verified:
        await message.answer(ui.incorrect_verification_code_msg)
        return
    await message.answer(
        ui.get_greeting(message.from_user.full_name),
        reply_markup=ui.info_keyboard,
    )


@dp.callback_query(lambda c: c.data == "vmi")
async def vmi_handler(callback_query: CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    vmi_number = utils.get_vmi_number(user_id)
    await callback_query.message.answer(ui.get_vmi_msg(vmi_number))


@dp.callback_query(lambda c: c.data == "salary_days")
async def salary_days_handler(callback_query: CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    first_day, second_day = utils.get_salary_days(user_id)
    await callback_query.message.answer(ui.get_salary_days_msg(first_day, second_day))


@dp.callback_query(lambda c: c.data == "vacation_days")
async def vacation_days_handler(callback_query: CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    vacation_days = utils.get_vacation_days(user_id)
    await callback_query.message.answer(ui.get_vacation_days_msg(vacation_days))


async def main() -> None:
    bot = Bot(
        settings.bot_token.get_secret_value(),
        parse_mode=ParseMode.HTML,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
