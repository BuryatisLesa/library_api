from sqlalchemy  import Column, Integer, String, Boolean
from app.db.base_class import Base


class Reader(Base):
    __tablename__ =  "readers"

    # структура таблицы читателей
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    active = Column(Boolean, default=True)