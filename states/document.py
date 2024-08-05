from aiogram.dispatcher.filters.state import State, StatesGroup

class DocumentCreateStorage(StatesGroup):
    """
    Класс машины состояний для создания документов
    """
    name = State()
    iban = State()
    date_birth = State()
    sex = State()
