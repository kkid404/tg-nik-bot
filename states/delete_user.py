from aiogram.dispatcher.filters.state import State, StatesGroup

class UserDeleteStorage(StatesGroup):
    """
    Класс машины состояний для удаления пользователя
    """
    name = State()
