from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import config
from buttons import *
import emoji
import sql
import states as st
import datetime

sendApplication = Router()
bot = Bot(config.TOKEN)


@sendApplication.callback_query(F.data == "but_user_sendApplication")
async def request_one(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.edit_text(text="Отправка заявки!", reply_markup=None)
    await cb.message.answer(text=f"Выберете отдел{emoji.emojize(':backhand_index_pointing_down:')}",
                            reply_markup=button_select_otdel)
    await state.set_state(st.SendA.otdel)


@sendApplication.callback_query(lambda c: c.data.startswith("check_send_"))
async def request_two(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    a = cb.data.split("_")[-1]
    res = config.otdel[int(a)]
    await state.update_data(otdel=res)
    await cb.message.answer(f"Напишите номер кабинета:")
    await state.set_state(st.SendA.cab)


@sendApplication.message(st.SendA.cab)
async def request_free(mes: Message, state: FSMContext):
    await state.update_data(cab=mes.text)
    await mes.answer("Опишите проблему:")
    await state.set_state(st.SendA.opis)


@sendApplication.message(st.SendA.opis)
async def request_four(mes: Message, state: FSMContext):
    await state.update_data(opis=mes.text)
    res = await state.get_data()
    send = sql.send_application(
        username=sql.search_user(mes.from_user.id)[0][1],
        cab=res["cab"],
        opis=res["opis"],
        otdel=res["otdel"],
        date=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    await mes.answer("Заявка отправлена!\n"
                     f"Имя - {sql.search_user(mes.from_user.id)[0][1]}\n"
                     f"Кабинет - {res['cab']}\n"
                     f"Описание - {res['opis']}\n"
                     f"Отдел - {res['otdel']} отдел\n"
                     f"Время - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                     f"Статус - Отправлена\n"
                     f"Номер заявки - {send[0]}", reply_markup=delete_application_1)
    print(send[1])  # Информация об отправлении заявки, выведет ошибку если не отправилась

    rab = sql.get_otdel(res['otdel'])
    for itt in range(0, len(rab[0])):
        await bot.send_message(rab[0][itt], "Пришла заявка", reply_markup=button_otdel)

    await state.clear()


@sendApplication.callback_query(F.data == "user_delete_application")
async def user_delete(cb: CallbackQuery):
    await cb.answer()
    num = cb.message.text.split("-")[-1]

    id = sql.delete_application_user(int(num))
    if id == "Выполнена" or id == "Удалена":
        await cb.message.answer(f"Заявка под номером {num} уже выполнена или удалена, вы не можете её удалить")
    elif id == "Not Started":
        await cb.message.answer(f"Вы удалили заявку номер {num}")
    else:
        await bot.send_message(id, f"К сожалению пользователь удалил заявку номер {num}")
        await cb.message.answer(f"Вы удалили заявку номер {num}")


@sendApplication.callback_query(F.data == "get_application_user")
async def get_application_user(cb: CallbackQuery):
    await cb.answer()
    id_user = cb.message.chat.id
    mas_applications = sql.get_applications_user(id_user)
    if len(mas_applications) == 0:
        await cb.message.answer("У вас нет активных заявок")
    for i in range(0, len(mas_applications)):
        mas = mas_applications[i]
        mes_text = f"Имя - {mas[1]}\n" \
                   f"Кабинет - {mas[2]}\n" \
                   f"Описание - {mas[3]}\n" \
                   f"Отдел - {mas[4]} отдел\n" \
                   f"Время - {mas[5]}\n" \
                   f"Статус - {mas[6]}\n" \
                   f"Выполняет - {mas[7]}\n" \
                   f"Номер заявки - {mas[0]}"
        await cb.message.answer(f"{mes_text}", reply_markup=delete_application_1)
