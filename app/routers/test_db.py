from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db

router = APIRouter()

# тестовый роутер для проверки БД
@router.get("/ping-db")
def ping_db(db: Session = Depends(get_db)):
    return{"message":"База подключена и работает."}