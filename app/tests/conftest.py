import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base_class import Base
from app.main import app
from app.db.deps import get_db
from app.models.book import Book
from app.models.reader import Reader
from app.models.user import User
from app.core.security import get_password_hash

# создаёт временную тестовую базу данных на sqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# создаёт движок подключения к базе
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# создаёт сессию для подключения к базе
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# переопределяет зависимость get_db на тестовую
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# подменяет зависимость во всём приложении
app.dependency_overrides[get_db] = override_get_db

# создаёт тестовый клиент fastapi и заполняет тестовые данные
@pytest.fixture(scope="module")
def client():
    # удаляет старые таблицы и создаёт новые
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    # добавляет книги
    db.add_all([
        Book(id=1, title="Book1", author="Author1", copies_available=3),
        Book(id=2, title="Book2", author="Author2", copies_available=1),
        Book(id=3, title="Book3", author="Author3", copies_available=0),
    ])

    # добавляет читателей
    db.add_all([
        Reader(id=1, name="Reader One", email="reader1@example.com"),
        Reader(id=2, name="Reader Two", email="reader2@example.com"),
    ])

    # добавляет пользователя
    user = User(
        id=1,
        email="user@test.com",
        hashed_password=get_password_hash("password")
    )
    db.add(user)
    db.commit()
    db.close()

    yield TestClient(app)
