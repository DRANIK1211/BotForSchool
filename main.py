from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import asyncio
import logging

import states
# Импортируем модули
from reg import registration
from sendApplication import sendApplication
from getApplicationsOtdel import getApplication
from convertToExcel import convert
from config import *
import sql
import textMessages as tM
import buttons as btn
bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(mes: Message):
    global but
    user = sql.search_user(mes.from_user.id)
    # Ищем в таблице users людей с id, в ответе массив [id, username, role, count]
    if user:  # Проверяем пустой ли массив
        role = user[0][2]
    else:
        await mes.answer(tM.messageStart_userNull, reply_markup=btn.button_registration)
        return

    match role:  # Проверяем роль пользователя и выводим соответствующие кнопки
        case "Учитель":
            but = btn.button_user
        case "Админ":
            but = btn.button_admin
        case "ИТ":
            but = btn.button_otdel
        case "Хозяйственный":
            but = btn.button_otdel
        case _:
            await mes.answer("Ошибка роли пользователя. Обратитесь в поддержку")

    await mes.answer(tM.messageStart, reply_markup=but)
    sql.add_app()


@dp.callback_query(F.data == "but_admin_deleteUser")
async def delete(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.answer("Введите id пользователя:")
    await state.set_state(states.Del.id)


@dp.message(Command("delete"))
async def delete(mes: Message, state: FSMContext):
    await mes.answer("Введите id пользователя:")
    await state.set_state(states.Del.id)


@dp.message(states.Del.id)
async def delete1(mes: Message, state: FSMContext):
    id = int(mes.text)
    user = sql.search_user(id)
    if user == []:
        await mes.answer("Пользователя с таким id не существует")
    else:
        sql.delete(id)
        await mes.answer(f"Вы удалили пользователя с именем {user[0][1]}")
    await state.clear()


async def run_bot():
    dp.include_router(registration)
    dp.include_router(sendApplication)
    dp.include_router(getApplication)
    dp.include_router(convert)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Удалить после разработки
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("EXIT")
