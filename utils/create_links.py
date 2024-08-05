from datetime import datetime
from aiogram import types
from aiogram.utils.markdown import hcode
import requests

from models import Keitaro
from data import LinkService, Link, OldLink, UserService
from loader import bot, ADMIN
from keyboard import ClientKeyboard
import requests


async def create_link(message: types.Message, token: str, request: str) -> bool:
    """
    Создает ссылку для выбранной пользователем кампании.

    Args
    -------
    message : types.Message 
    Класс aiogram для отправки сообщений

    token : str
    Токен пользователя из кейтаро

    request : str
    Название кампании из кейтаро

    Returns
    -------
    True: если компания найдена
    
    False: если компания не найдена
    """
    try: 
        link = Link
        old_link = OldLink
        treker = Keitaro(token)
        campanies = await treker._get_all_keitaro_campaigns()
        for campany in campanies:
            if request == campany["name"]:
                if len(LinkService.get(link)) == 0:
                    ready_link = LinkService.get(old_link, 1)
                else:
                    ready_link = LinkService.get(link, 1)
                    LinkService.delete(link, ready_link)
                    LinkService.add(old_link, ready_link)
                
                clone_data = await treker.clone_campaign(campany['id'])

                if not clone_data:
                        raise Exception(f"Empty clone data dict! requested company: {campany['id']}")
            
                name = clone_data[0]['name']
                campany_id = clone_data[0]['id']
                
                if str((message.from_user.id)) != ADMIN[0]:
                    name_sub1 = UserService.get_by_id(message.from_user.id).sub
                else:
                    name_sub1 = "admin"

                index = name.find('Copy #')
                name = name[:index]
                name = name + f'BOT-COPY {name_sub1}'
                name = name.replace('Основа', str(datetime.now()))
                new_campany = await treker.rename_campaign(campany_id, name)

                if not new_campany:
                    raise Exception(
                        f"Empty dict after rename! requested company: {campany['id']}; CHAT_ID: {message.chat.id}")
                
                link = f'{ready_link}/{new_campany["alias"]}'

                try:
                    response = requests.get(link)
                    if response.status_code != 200:
                        await bot.send_message(
                            message.chat.id, 
                            f"Ошибка при создании ссылки\nпопробуйте еще раз",
                            reply_markup=ClientKeyboard().start_kb(),
                        )
                        LinkService.delete(old_link, ready_link)
                        return True
                except requests.exceptions.RequestException as e:
                    await bot.send_message(
                        message.chat.id, 
                        f"Ошибка при создании ссылки\nпопробуйте еще раз",
                        reply_markup=ClientKeyboard().start_kb(),
                    )
                    LinkService.delete(old_link, ready_link)
                    return True


                subs = {}
                for sub in new_campany['parameters']:
                    if sub in ['extra_param_1', 'extra_param_2', 'extra_param_3', 'extra_param_4']:
                        continue
                    if new_campany['parameters'][sub]['placeholder'] == '':
                        continue
                    subs[new_campany['parameters'][sub]["name"]] = new_campany['parameters'][sub]['placeholder']
                if len(subs) != 0:
                    link += '?'
                    for sub in subs:
                        if sub == 'sub1':
                            link += f'sub1={name_sub1}'
                        else:
                            link += f'{sub}={subs[sub]}'
                        link += '&'
                    link = link.replace("fbclid={fbclid}&", "")
                    link = link[0:-1]
                
                msg = (f'ID кампании:\n<b>{new_campany["id"]}</b>\n\n'
                    f'Имя кампании:\n<b>{new_campany["name"]}</b>\n\n'
                    f'Ссылка:\n{hcode(link)}')

                if new_campany["notes"] != '':
                    msg += (f'\n\nОписание:\n{new_campany["notes"]}')

                await bot.send_message(
                    message.chat.id, 
                    msg,
                    reply_markup=ClientKeyboard().start_kb(),
                    parse_mode='HTML'
                    )

                return True
            else:
                continue
        return False
    except Exception as e:
        print(e)