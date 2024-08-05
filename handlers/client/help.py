from aiogram import types

from loader import dp, bot
from loader import SUPPORT
from keyboard import ClientKeyboard

@dp.message_handler(commands=['help'])
async def start_message(message: types.Message):
        bot.send_message(
            message.chat.id, 
            'Если бот не даёт вам ссылку,\n'
            'В первую очередь нажмите кнопку "Обновить" '
            f'или /start\nПри возниковении других проблем пишите {SUPPORT}',
            reply_markup=ClientKeyboard().start_kb()
        )
