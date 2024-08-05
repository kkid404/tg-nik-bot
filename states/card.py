from aiogram.dispatcher.filters.state import State, StatesGroup

class CardCreateStorage(StatesGroup):
    """
    Класс машины состояний для создания карты
    """
    name = State()
    number = State()
    date = State()
    cvv = State()


