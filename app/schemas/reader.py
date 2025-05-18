from pydantic import BaseModel, EmailStr


class ReaderCreate(BaseModel):
    name: str
    email: EmailStr


class ReaderOut(BaseModel):
    id:int
    name: str
    email: EmailStr
    active:bool


    class Config:
        from_attributes = True


class ReaderUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    active: bool | None = None

