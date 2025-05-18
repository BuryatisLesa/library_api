from sqlalchemy  import Column, Integer, String, Boolean
from app.db.base_class import Base


class Book(Base):
    __tablename__ = "books"


    # структура для таблицы books
    id = Column(Integer, primary_key=True, index = True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    available = Column(Boolean, default=True)