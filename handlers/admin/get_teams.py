from aiogram import types
from aiogram.dispatcher.filters import IDFilter

from loader import dp, bot, ADMIN
from models import Keitaro

@dp.message_handler(IDFilter(chat_id=ADMIN[:]), commands=['team'])
async def links(message: types.Message):
    res = await Keitaro.get_all_campanies_users()
    for k,v in res.items():
        await bot.send_message(
            message.from_user.id,
            f"{k}\n{v}"
        )