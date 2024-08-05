from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types

from loader import ADMIN
from data import UserService


class UserMiddleware(BaseMiddleware):
    """
    Контролирует доступ к боту, 
    если пользователя нет в базе данных 
    или администраторах, не будет ему отвечать.
    """
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = str(update.message.from_user.id)
        elif update.callback_query:
            user = str(update.callback_query.from_user.id)
        else:
            return
        
        if user not in UserService.get_all()["chat_id"] and user not in ADMIN:
            raise CancelHandler()