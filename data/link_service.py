import random
from data.data import session
from typing import Union

"""
Модуль для взамодействия с классами ссылок.
"""

class LinkService:
    """
    Класс для работы с ссылками.
    В БД содержиться две таблицы:
    1. Link:
    -------
        Содержит новые ссылки, которые еще не выдавались баерам
    
    2. OldLink:
    -------
        Содержит ссылки, которые использовались хотя бы один раз.

    Methods:
    -------
    - add(object, link)
    добавляет ссылку в базу данных.
    
    - get(object)
    возвращает список ссылок из базы данных.
    """

    @staticmethod
    def add(object ,link: str) -> None:
        """
        Добавляет новую ссылку в базу данных.

        Args:
        -------
            object (class): класс ссылки.
            link: str: ссылка на домен

        Return:
        ------- 
            None
        """
        link = object(link=link)
        session.add(link)
        session.commit()

    @staticmethod
    def get(object, count: int = 0) -> Union[list, str]:
        """
        Получить все ссылки из базы данных.

        Args:
        -------
            object (class): класс ссылки.
            count (int, optional): параметр, который опреляет, сколько вернуть ссылок

        Return:
        -------
            list: список ссылок.
            str: ссылка.
        """
        ready_links = []
        links = session.query(object).all()
        for link in links:
            ready_links.append(link.link)
        if count == 0:
            return ready_links
        else:
            return random.choice(ready_links)
    
    @staticmethod
    def delete(object, link: str) -> None:
        r_link = session.query(object).filter(object.link == str(link)).first()
        session.delete(r_link)
        session.commit()