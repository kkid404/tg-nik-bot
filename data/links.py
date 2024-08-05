from sqlalchemy import Column, Integer, String

from data.data import Base

"""
Базовая модель новых ссылок SQLAlchemy для базы данных.
"""

class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    link = Column(String(100), unique=True, nullable=False)
