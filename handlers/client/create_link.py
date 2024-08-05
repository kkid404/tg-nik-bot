import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import  CreateLinksStorage
from data import LinkService, Link, OldLink
from keyboard import ClientKeyboard


@dp.message_handler(text='Заменить домен')
async def set_offers(message: types.Message, kb = ClientKeyboard()):
    await bot.send_message(
        message.from_user.id,
        f'Отправь мне ссылку на кампанию и я поменяю в ней домен:',
        reply_markup=kb.back()
        )

    await CreateLinksStorage.link.set()

@dp.message_handler(state=CreateLinksStorage.link)
async def get_offers(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    async with state.proxy() as data:
        data["link"] = message.text
    
    url_regex = re.compile(r'https?://')
    link = Link
    old_link = OldLink
    if url_regex.search(data["link"]):
        link_end = data["link"].split('/')[-1]
        
        if len(LinkService.get(link)) == 0:
                ready_link = LinkService.get(old_link, 1)
        else:
            ready_link = LinkService.get(link, 1)
            LinkService.delete(link, ready_link)
            LinkService.add(old_link, ready_link)
        
        await bot.send_message(
             message.from_user.id, 
             f'Твоя ссылка с новым доменом:\n\n`{ready_link}/{link_end}`',
             reply_markup=kb.start_kb(),
             parse_mode = 'Markdown'
             )
        await state.finish()
    else:
        await bot.send_message(
             message.from_user.id, 
             f'Отправлена не ссылка.\nПопробуй еще раз.'
        )

