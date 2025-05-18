from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# настройки безопасности

ALGORITHM = "HS256"

SECRET_KEY = "my_secret_key"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# генерация JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))

    to_encode.update({"exp": expire})
    encode_jwt =  jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


# контекст хеширования с алгоритмом bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# создание хэша для пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# провериряем верификацию пароля / проверка соответствия хэша == пароль
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

