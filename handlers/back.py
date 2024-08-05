# back.py
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from keyboard import ClientKeyboard as Keyboard

@dp.message_handler(Text(equals='⬅️ Назад ⬅️', ignore_case=True), state='*')
async def cancel_handlers(message: types.Message, state: FSMContext):
    kb = Keyboard()  # Переносим создание экземпляра сюда
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(
        message.from_user.id,
        'Хорошо!', 
        reply_markup=kb.start_kb())

@dp.message_handler(Text(equals='На главную', ignore_case=True))
async def cancel_handlers(message: types.Message, state: FSMContext):
    kb = Keyboard()  # Переносим создание экземпляра сюда
    await bot.send_message(
        message.from_user.id,
        'Хорошо!', 
        reply_markup=kb.start_kb())
