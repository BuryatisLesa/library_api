from pydantic import BaseModel


# входные данные от пользователя/сотрудник
class BookCreate(BaseModel):
    title: str
    author: str

# ответ пользователю/сотруднику
class BookOut(BaseModel):
    id:int
    title: str
    author: str
    available: bool

    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    available: bool | None = None
    
