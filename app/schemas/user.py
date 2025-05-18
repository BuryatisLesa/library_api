from pydantic import BaseModel, EmailStr


# проверка входных данных при создание регистрации пользователя
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# ответ пользователю
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True  # для работы с ORM sqlalchemy-объектами
