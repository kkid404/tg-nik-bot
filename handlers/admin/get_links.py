from aiogram import types
from aiogram.dispatcher.filters import IDFilter

from loader import ADMIN, dp, bot
from data import Link, LinkService, OldLink

@dp.message_handler(IDFilter(chat_id=ADMIN[:]), commands=['links'])
async def links_message(message: types.Message):
    link = Link
    old_link = OldLink
    await bot.send_message(
        message.chat.id, 
        f'Свежих доменов: {len(LinkService.get(link))}\n'
        f'Старых доменов: {len(LinkService.get(old_link))}',
        )
