from passlib.context import CryptContext

# контекст хеширования с алгоритмом bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# создание хэша для пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# провериряем верификацию пароля / проверка соответствия хэша == пароль
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)