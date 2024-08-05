from keyboard.keyboard import Keyboard
from models import Keitaro
from lang.ru import files


"""
Клавиатура для пользователя
"""

class ClientKeyboard(Keyboard):

    def start_kb(self):
        return self._keyboard(files["keyboards"]["main"])
    
    async def offers_kb(self, token):
        treker = Keitaro(token)
        btns = await treker.get_user_campany()
        btns.append('🔄 Обновить 🔄')
        btns.append('⬅️ Назад ⬅️')
        return self._keyboard(btns, 1)
    
    def country_kb(self):
        return self._keyboard(files["keyboards"]["country"])

    def documents_kb(self):
        return self._keyboard(files["keyboards"]["documents"])
    
    def sex_kb(self):
        return self._keyboard(files["keyboards"]["sex"])
