from sqlalchemy import Column, Integer, String

from data.data import Base

"""
Базовая модель использованных ссылок SQLAlchemy для базы данных.
"""

class OldLink(Base):
    __tablename__ = 'old_links'
    id = Column(Integer, primary_key=True)
    link = Column(String(100), unique=True, nullable=False)

        
