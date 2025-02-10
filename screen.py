# для скринов
@dp.message(CommandStart())
async def start(mes: Message):
     
    await mes.answer(tM.messageStart, reply_markup=but)
