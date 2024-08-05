from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import OfferStorage
from data import UserService
from keyboard import ClientKeyboard
from utils import create_link
from loader import ADMIN, KEIARO_ADMIN_TOKEN


@dp.message_handler(text='🔄 Обновить 🔄')
async def set_offers_update(message: types.Message, kb = ClientKeyboard()):
    if str(message.from_user.id) == ADMIN[0]:
        token = KEIARO_ADMIN_TOKEN
    else:
        token = UserService.get_by_id(message.from_user.id).token
    await bot.send_message(
        message.from_user.id,
        f'Список кампаний:',
        reply_markup=await kb.offers_kb(token)
        )

    await OfferStorage.offer.set()

@dp.message_handler(text='Выбрать кампанию')
async def set_offers(message: types.Message, kb = ClientKeyboard()):
    if str(message.from_user.id) == ADMIN[0]:
        token = KEIARO_ADMIN_TOKEN
    else:
        token = UserService.get_by_id(message.from_user.id).token
    await bot.send_message(
        message.from_user.id,
        f'Список кампаний:',
        reply_markup=await kb.offers_kb(token)
        )

    await OfferStorage.offer.set()

@dp.message_handler(state=OfferStorage.offer)
async def get_offers(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    async with state.proxy() as data:
        data["offer"] = message.text
    if str(message.from_user.id) == ADMIN[0]:
        token = KEIARO_ADMIN_TOKEN
    else:
        token = UserService.get_by_id(message.from_user.id).token
    if data["offer"] != '🔄 Обновить 🔄':
        res = await create_link(message, token, data["offer"])
        if res == True:
            await state.finish()
        else:
            await bot.send_message(
                message.from_user.id,
                'Ошибка при создании ссылки. Выбери кампанию из списка ниже:',
                reply_markup=await kb.offers_kb(token)
                )
    else:
        await bot.send_message(message.chat.id, 'Список кампаний:', reply_markup=await kb.offers_kb(token))
        await OfferStorage.offer.set()