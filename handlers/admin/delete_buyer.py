from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter

from loader import dp, bot
from states import UserDeleteStorage
from keyboard import AdminKeyboard
from loader import ADMIN
from data import UserService

@dp.message_handler(IDFilter(chat_id=ADMIN[:]), text="Удалить баера")
async def delete_buyer(message: types.Message, state: FSMContext, kb = AdminKeyboard()):
    await bot.send_message(
        message.from_user.id,
        "Выберите имя баера:",
        reply_markup=kb.all_users_kb()
    )
    await UserDeleteStorage.name.set()

@dp.message_handler(state=UserDeleteStorage.name)
async def delete_name(message: types.Message, state: FSMContext, kb = AdminKeyboard()):
    async with state.proxy() as data:
        data['name'] = message.text
    
    res = data["name"].split("-")
    res = UserService.get_by_name_and_sub(res[0], res[1])
    UserService.delete(res)
    await bot.send_message(
        message.from_user.id,
        f"Вы успешно удалили баера {message.text}",
        reply_markup=kb.start_kb()
    )
    await state.finish()