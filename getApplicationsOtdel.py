from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import config
from buttons import *
import sql
import states as st
import emoji

getApplication = Router()
bot = Bot(config.TOKEN)


@getApplication.callback_query(F.data == "but_otdel_getApplications")
async def get_application_otdel(cb: CallbackQuery):
    await cb.answer()
    id_user = cb.message.chat.id
    mas_applications = sql.get_applications_otdel(id_user)
    if len(mas_applications) == 0:
        await cb.message.answer("Нет активных заявок")
    for i in range(0, len(mas_applications)):
        mas = mas_applications[i]
        mes_text = f"Имя - {mas[1]}\n" \
                   f"Кабинет - {mas[2]}\n" \
                   f"Описание - {mas[3]}\n" \
                   f"Время - {mas[5]}\n" \
                   f"Номер заявки - {mas[0]}"
        await cb.message.answer(f"{mes_text}", reply_markup=button_otdel_for_application)


@getApplication.callback_query(F.data == "otdel_answer_application")
async def otdel_answer_application(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(st.Answer.id)
    await state.update_data(id=int(cb.message.text.split("-")[-1]))

    await cb.message.answer(f"Ответ на заявку номер {int(cb.message.text.split('-')[-1])}\n"
                            f"Пожалуйста, напишите, что вы хотите написать отправителю:")

    await state.set_state(st.Answer.answer)


@getApplication.message(st.Answer.answer)
async def otdel_answer(mes: Message, state: FSMContext):
    await state.update_data(answer=mes.text)
    data = await state.get_data()
    status = sql.get_status_application(data["id"])

    if status[0] == "Выполнена" or status[0] == "Удалена":
        await mes.answer("Заявка была выполнена или удалена, вы не можете ответить на неё")
        await state.clear()
    elif status[0] == "Отправлена":
        sql.execute_application(mes.from_user.id, data["id"])
        await bot.send_message(status[1],
                               f"Вы получили сообщение, номер заявки {data['id']}\nВаша заявка была выполнена\n\n"
                               f"{data['answer']}", reply_markup=button_user)
        await mes.answer("Мы отправили ваше сообщение\nВы выполнили заявку", reply_markup=button_otdel)
        sql.execute_application_finish(data["id"])
        await state.clear()
    else:
        await mes.answer(f"Неизвестная ошибка\n{status}")
        await state.clear()


@getApplication.callback_query(F.data == "otdel_take_over_applications")
async def otdel_take_over_applications(cb: CallbackQuery):
    await cb.answer()
    id_application = int(cb.message.text.split("-")[-1])
    status = sql.get_status_application(id_application)

    if status[0] == "Выполнена" or status[0] == "Удалена":
        await cb.message.answer("Заявка была выполнена или удалена, вы не можете ответить на неё")
    elif status[0] == "Отправлена":
        sql.execute_application(cb.message.chat.id, id_application)
        await cb.message.answer(f"Вы взяли в работу заявку - {id_application}\n"
                                f"Когда заявка будет выполнена нажмите кнопку {emoji.emojize(':backhand_index_pointing_down:')}",
                                reply_markup=button_otdel_finish_work)
        await bot.send_message(status[1], f"Вашу заявку взяли в работу\nНомер заявки - {id_application}")

    elif status[0] == "Выполняется":
        await cb.message.answer(f"Кто-то уже выполняет эту заявку", reply_markup=button_otdel)
    else:
        await cb.message.answer(f"Неизвестная ошибка\n{status}")


@getApplication.callback_query(F.data == "otdel_finish_work")
async def otdel_take_over_applications(cb: CallbackQuery):
    await cb.answer()
    id_applications = int(cb.message.text.split("\n")[0].split("-")[-1])
    sql.execute_application_finish(id_applications)
    id_user = sql.search_id(id_applications)
    await cb.message.answer(f"Вы выполнили заявку номер {id_applications}", reply_markup=button_otdel)
    await bot.send_message(id_user, f"Вашу заявку выполнили\nНомер заявки - {id_applications}", reply_markup=button_user)
