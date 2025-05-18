from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message":f"Привет {current_user.email}! Ты авторизован."}