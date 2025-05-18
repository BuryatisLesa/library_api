from app.db.session import SessionLocal
from sqlalchemy.orm import Session


def get_db() -> Session:
    db = SessionLocal() #создаем сессию
    try:
        yield db
    finally:
        db.close()
