from keyboard.keyboard import Keyboard
from data import UserService

"""
Клавиатура для администратора
"""

class AdminKeyboard(Keyboard):

    def start_kb(self):
        kb = self._keyboard(['Добавить баера', 'Удалить баера', 'Добавить домены'])
        btn_back = 'На главную'
        kb.add(btn_back)
        return kb
    
    def all_users_kb(self):
        ready_btn = []
        for name, sub in zip(UserService.get_all()['names'], UserService.get_all()['subs']):
            ready_btn.append(f"{name}-{sub}")
        ready_btn.append('⬅️ Назад ⬅️')
        return self._keyboard(ready_btn, 1)