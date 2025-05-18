from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.db.deps import get_db
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # проверка на наличие пользователя с email в бд
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Пользователь с таким email уже зарегистрирован"
        )
    
    # хеширование пароля
    hashed_password = get_password_hash(user.password)


    # cоздаем пользователя
    new_user = User(email = user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
