from typing import Union

from sqlalchemy import Column, Integer, String

from data.data import session, Base

"""
Модуль в котором определяется модель User в базе данных 
и класс UserService для управления данными.
"""

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    chat_id = Column(String(30), nullable=False, unique=True)
    sub = Column(String(30), nullable=True, unique=True)
    token = Column(String(100), nullable=True)

class UserService:

    @staticmethod
    def add(chat_id: str, token: str, sub: str) -> int:
        """
        Добавляет пользователя в базу данных

        Args:
        -------
            chat_id: str
            телеграм id пользователя
            
            token: str
            токен пользователя из Кейтаро

            sub: str
            арбитражный никнейм пользователя
            
            name: str
            имя пользователя телеграм
        
        Returns:
        -------
            id созданного пользователя
        """
        user = User(chat_id=str(chat_id), token=str(token), sub=str(sub))
        session.add(user)
        session.commit()
        return user.id

    @staticmethod
    def update(telegram_id: str, name: str) -> None:
        """
        Обновляет информацию о пользовате в базе данных

        Args:
        -------
            telegram_id: str
            id пользователя в телеграме
            
            name: str
            Имя пользователя в телеграме
        
        Returns:
        -------
            None
        """
        user = session.query(User).filter(User.chat_id == str(telegram_id)).first()
        user.name = name
        session.commit()

    @staticmethod
    def get_by_name_and_sub(name: str, sub: str) -> Union[str, bool]:
        """
        Возвращает телеграм id пользователя по имени и арбитражному никнейму

        Args:
        -------
            name: str
            Имя пользователя в телеграме

            sub: str
            Арбитражный никнейм пользователя
        
        Returns:
        -------
            user.chat_id: телеграм id пользователя
            False: если пользователь не найден
        """
        if name == "None":
            name = None
        user = session.query(User).filter(User.name == name, User.sub == str(sub)).first()
        return user.chat_id if user else False

    @staticmethod
    def get_by_id(chat_id: str) -> Union[User, bool]:
        """
        Возвращает информацию о пользовате в базе данных

        Args:
        -------
            chat_id: str
            телеграм id пользователя
        
        Returns:
        -------
            User: класс пользователя
            False: если пользователь не найден
        """
        user = session.query(User).filter(User.chat_id == str(chat_id)).first()
        if user:
            return user
        else:
            return False
    
    @staticmethod
    def get_all() -> dict:
        """
        Возвращает информацию о всех пользователях в базе данных

        
        Returns:
        -------
            Словарь: список всех полей пользователей из базы данных
        """
        chat_ids = []
        subs = []
        names = []
        tokens = []
        users = session.query(User).all()
        for user in users:
            chat_ids.append(user.chat_id)
            names.append(user.name)
            subs.append(user.sub)
            tokens.append(user.token)
        return {"chat_id" : chat_ids, "subs" : subs, "names" : names, "tokens" : tokens}
    
    @staticmethod
    def delete(chat_id: str) -> None:
        """
        Удаляет пользователя из базы данных

        Args:
        -------
            id: int
            id пользователя в базе данных
        
        Returns:
        -------
            None
        """
        user = session.query(User).filter(User.chat_id == str(chat_id)).first()
        session.delete(user)
        session.commit()