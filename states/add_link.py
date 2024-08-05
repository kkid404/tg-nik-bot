from aiogram.dispatcher.filters.state import State, StatesGroup

class LinksStorage(StatesGroup):
    """
    Класс машины состояний для ссылок
    """
    link = State()