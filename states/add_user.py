from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStorage(StatesGroup):
    """
    Класс машины состояний для пользователя
    """
    chat_id = State()
    sub = State()
    token = State()