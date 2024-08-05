from aiogram import types
from aiogram.dispatcher.filters import IDFilter

from loader import ADMIN, dp, bot
from models import Keitaro



@dp.message_handler(IDFilter(chat_id=ADMIN[:]), commands=['campaigns'])
async def get_campanings(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "Подготавливаю..."
    )
    await bot.send_message(
        message.from_user.id,
        await Keitaro.get_all_campanies(),
    )