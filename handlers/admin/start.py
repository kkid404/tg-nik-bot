from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter

from loader import dp, bot, ADMIN
# from data import UserService
from keyboard import AdminKeyboard

"""
Стартовый хэндлер
"""

@dp.message_handler(IDFilter(chat_id=ADMIN[:]), commands=['admin'])
async def start(message: types.Message, kb = AdminKeyboard()):
    await bot.send_message(
        message.from_user.id,
        f"Добро пожаловать, {message.from_user.first_name}!",
        reply_markup=kb.start_kb()
        )