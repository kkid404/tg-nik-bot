from aiogram import types

from loader import dp, bot
from data import UserService
from keyboard import ClientKeyboard

"""
Стартовый хэндлер
"""

@dp.message_handler(commands=['start'])
async def start(message: types.Message, kb = ClientKeyboard()):
    res = UserService.get_by_id(message.from_user.id)
    if res != False:
        if res.name == None:
            UserService.update(message.from_user.id, message.from_user.first_name)
    
    hello_message = "*Условия для вас:*\n\n"\
    "- Мы предоставляем повышенную ставку, чтобы обеспечить вас высокими доходами.\n"\
    "- Заключаем надежные партнерские соглашения и интегрируемся с ответственными партнерами.\n"\
    "- Поможем полностью собрать сетап для эффективного запуска наших оферов.\n"\
    "- Предоставляем примеры успешных креативов, которые в данный момент показывают отличные результаты.\n"\
    "- Выплаты производятся по вашему запросу, чтобы обеспечить удобство и комфорт в работе.\n"\
    "\n\n*Что мы ожидаем от вас:*\n\n"\
    "- При работе с нашими оферами, ожидаем ответственного и профессионального подхода.\n"\
    "- Важно выполнять обозначенные цели и KPI для успешного сотрудничества.\n"\
    "- При возможности, увеличивайте объемы продвижения, и это поможет нам повысить ставки и вашу прибыль.\n"\

    await bot.send_message(
        message.from_user.id,
        hello_message,
        reply_markup=kb.start_kb(),
        parse_mode='Markdown'
        )