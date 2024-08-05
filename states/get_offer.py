from aiogram.dispatcher.filters.state import State, StatesGroup

class OfferStorage(StatesGroup):
    """
    Класс машины состояний для ключа кейтаро
    """
    offer = State()