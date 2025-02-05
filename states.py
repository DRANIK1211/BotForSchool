# Состояния для разных последовательных действий

from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    name = State()
    role = State()


class SendA(StatesGroup):
    otdel = State()
    cab = State()
    opis = State()


class Answer(StatesGroup):
    id = State()
    answer = State()


class Del(StatesGroup):
    id = State()
