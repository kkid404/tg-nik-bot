from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter

from loader import dp, bot, ADMIN
from states import UserStorage
from keyboard import AdminKeyboard
from data import UserService

@dp.message_handler(IDFilter(chat_id=ADMIN[:]), text="Добавить баера")
async def add_buyer(message: types.Message, kb = AdminKeyboard()):
    await bot.send_message(
        message.from_user.id, 
        "Введите телеграм id баера:",
        reply_markup=kb.back()
        )
    await UserStorage.chat_id.set()

@dp.message_handler(state=UserStorage.chat_id)
async def add_buyer_sub(message: types.Message, state: FSMContext, kb = AdminKeyboard()):
    async with state.proxy() as data:
        data['chat_id'] = message.text
    await bot.send_message(
        message.from_user.id, 
        "Введите sub1 баера:",
        reply_markup=kb.back()
    )
    await UserStorage.next()

@dp.message_handler(state=UserStorage.sub)
async def add_buyer_sub_sub(message: types.Message, state: FSMContext, kb = AdminKeyboard()):
    async with state.proxy() as data:
        data['sub'] = message.text
    await bot.send_message(
        message.from_user.id, 
        "Введите токен баера из Keitaro:",
        reply_markup=kb.back()
    )
    await UserStorage.next()

@dp.message_handler(state=UserStorage.token)
async def add_buyer_token(message: types.Message, state: FSMContext, kb = AdminKeyboard()):
    async with state.proxy() as data:
        data['token'] = message.text
    await bot.send_message(
        message.from_user.id, 
        "Баер добавлен!",
        reply_markup=kb.start_kb()
    )
    UserService.add(data['chat_id'], data['token'], data['sub'])
    await state.finish()