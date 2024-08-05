from aiogram.dispatcher.filters.state import State, StatesGroup

class CreateLinksStorage(StatesGroup):
    """
    Класс машины состояний для ссылок
    """
    link = State()