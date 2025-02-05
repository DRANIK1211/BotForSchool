from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
import sqlite3
import pandas as pd
import config

convert = Router()
bot = Bot(config.TOKEN)


@convert.callback_query(F.data == "but_admin_getReport")
async def but_admin_getReport(cb: CallbackQuery):
    await cb.answer()
    conn = sqlite3.connect('base.db')
    query1 = "SELECT * FROM users"
    df1 = pd.read_sql_query(query1, conn)
    query2 = "SELECT * FROM applications"
    df2 = pd.read_sql_query(query2, conn)
    conn.close()
    df1.to_excel('users.xlsx', index=False)
    df2.to_excel('applications.xlsx', index=False)

    user_id = cb.message.chat.id

    file_path = 'users.xlsx'  # Замените на путь к вашему файлу
    input_file = FSInputFile(file_path)  # Создаем InputFile из пути к файлу
    await cb.message.answer_document(document=input_file)

    file_path = 'applications.xlsx'  # Замените на путь к вашему файлу
    input_file = FSInputFile(file_path)  # Создаем InputFile из пути к файлу
    await cb.message.answer_document(document=input_file)

