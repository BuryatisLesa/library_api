from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.deps import get_db
from app.models.reader import Reader
from app.schemas.reader import ReaderCreate, ReaderOut, ReaderUpdate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

# создание нового читателя
@router.post("/readers", response_model=ReaderOut)
def create_reader(
    reader: ReaderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_reader = Reader(**reader.dict())
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)
    return new_reader

# получение всех имеющих читателей
@router.get("/readers", response_model=List[ReaderOut])
def get_readers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Reader).all()

# получение одного читателя
@router.get("/readers/{reader_id}", response_model=ReaderOut)
def get_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return reader

# удаление читателя
@router.delete("/readers/{reader_id}", response_model=ReaderOut)
def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    db.delete(reader)
    db.commit()
    return reader

# обновление данных читателя
@router.put("/readers/{reader_id}", response_model=ReaderOut)
def update_reader(
    reader_id: int,
    update_data: ReaderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(reader, field, value)

    db.commit()
    db.refresh(reader)
    return reader
