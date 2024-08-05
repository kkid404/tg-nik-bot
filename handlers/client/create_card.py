import re
import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.card import  CardCreateStorage
from keyboard import ClientKeyboard
from lang.ru import files
from models.adpos import Adpos

@dp.message_handler(text=files["keyboards"]["documents"][1])
async def create_card(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    await bot.send_message(
        message.from_user.id,
        files["messages"]["name"],
        reply_markup= kb.back()
    )
    await CardCreateStorage.name.set()

@dp.message_handler(state=CardCreateStorage.name)
async def get_name(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    
    async with state.proxy() as data:
        data["name"] = message.text

    await bot.send_message(
        message.from_user.id,
        files["messages"]["card"],
        reply_markup= kb.back()
    )

    await CardCreateStorage.next()

@dp.message_handler(state=CardCreateStorage.number)
async def get_card(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    
    async with state.proxy() as data:
        data["card"] = message.text

    await bot.send_message(
        message.from_user.id,
        files["messages"]["date_card"],
        reply_markup= kb.back()
    )

    await CardCreateStorage.next()


@dp.message_handler(state=CardCreateStorage.date)
async def get_date(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    
    async with state.proxy() as data:
        data["date"] = message.text

    await bot.send_message(
        message.from_user.id,
        files["messages"]["cvv"],
        reply_markup= kb.back()
    )

    await CardCreateStorage.next()

@dp.message_handler(state=CardCreateStorage.cvv)
async def get_cvv(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    
    async with state.proxy() as data:
        data["cvv"] = message.text
    
    bank = Adpos()
    number = data["card"]
    name = data["name"]
    date = data["date"]
    cvv = data["cvv"]

    ready_card = bank.create(number, name, date, cvv)
    open_card = open(ready_card, "rb")
    await bot.send_photo(
        message.from_user.id,
        open_card,
        reply_markup=kb.start_kb()
        )
    
    os.remove(ready_card)
    await state.finish()

    