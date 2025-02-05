#  Заготовки кнопок CallbackQuery

from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from config import otdel


button_registration = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            text="Зарегистрироваться",
            callback_data="but_registration"
        )
    ]]
)  # Кнопка регистрации


button_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Создать заявку", callback_data="but_user_sendApplication")],
        [InlineKeyboardButton(text="Посмотреть отправленные заявки", callback_data="get_application_user")]
    ]
)  # Кнопки User: отправка заявки, получение отправленных заявок


button_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Удалить пользователя", callback_data="but_admin_deleteUser")],
        [InlineKeyboardButton(text="Создать отчёт по заявкам", callback_data="but_admin_getReport")]
    ]
)  # Кнопки Admin: удаление пользователя, создание отчёта


button_otdel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть заявки", callback_data="but_otdel_getApplications")]
    ]
)  # Кнопки IT и Xoz: посмотреть пришедшие заявки

button_otdel_for_application = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ответить на заявку", callback_data="otdel_answer_application")],
        [InlineKeyboardButton(text="Взять заявку на себя", callback_data="otdel_take_over_applications")],
        [InlineKeyboardButton(text="Посмотреть заявки", callback_data="but_otdel_getApplications")]
    ]
)  # Кнопки IT и Xoz: кнопки для управления заявкой
button_otdel_finish_work = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Завершить работу", callback_data="otdel_finish_work")]
    ]
)  # Кнопки IT и Xoz: кнопки для управления заявкой


mus_otdel = []
for i in range(0, len(otdel)):
    mus_otdel.append(
        [InlineKeyboardButton(
            text=f"{otdel[i]} отдел",
            callback_data=f"check_send_{i}"
        )]
    )
button_select_otdel = InlineKeyboardMarkup(
    inline_keyboard=mus_otdel
)


delete_application_1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Удалить заявку", callback_data="user_delete_application")],
        [InlineKeyboardButton(text="Оставить заявку", callback_data="but_user_sendApplication")],
        [InlineKeyboardButton(text="Посмотреть заявки", callback_data="get_application_user")]
    ]
)