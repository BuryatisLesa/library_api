from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# url для подключение к sqllite
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

# создаем соединение с sqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}
    )

# создаем шаблон для подключение к БД при каждом запросе
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)