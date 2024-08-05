import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter

from loader import dp, bot, ADMIN
from states import LinksStorage
from keyboard import AdminKeyboard
from data import LinkService, Link

@dp.message_handler(IDFilter(ADMIN), text="Добавить домены")
async def link(message: types.Message, kb = AdminKeyboard()):
    await bot.send_message(
        message.from_user.id,
        "Пришли домены для добавления. Каждая домен должна быть с новой строки.",
        reply_markup=kb.back()
    )

    await LinksStorage.link.set()

@dp.message_handler(state=LinksStorage.link)
async def add_link(message: types.Message, state: FSMContext, kb = AdminKeyboard()):
    async with state.proxy() as data:
        data["link"] = message.text
    links = data["link"].split("\n")
    db_link = Link
    
    for link in links:
        url_regex = re.compile(r'https?://')
        if url_regex.search(link):
            LinkService.add(db_link, link)
            
            await bot.send_message(
                message.from_user.id,
                "Ссылки добавлены.",
                reply_markup=kb.start_kb()
            )
        else:
            await bot.send_message(
                message.from_user.id,
                f"Некорректный домен: {link}",
                reply_markup=kb.start_kb()
            )

    await state.finish()