from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.deps import get_db
from app.models.book import Book
from app.models.reader import Reader
from app.models.borrow import Borrow
from app.schemas.borrow import BorrowRequest, ReturnRequest, BorrowInfo
from app.core.deps import get_current_user
from app.models.user import User


router = APIRouter()
@router.post("/borrow", response_model=BorrowInfo)
def borrow_book(
    borrow_data: BorrowRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    book = db.query(Book).filter(Book.id == borrow_data.book_id).first()
    reader = db.query(Reader).filter(Reader.id == borrow_data.reader_id).first()

    if not book or not reader:
        raise HTTPException(status_code=404, detail="Книга или читатель не найдены")

    # экземпляры
    if book.copies_available < 1:
        raise HTTPException(status_code=400, detail="Нет доступных экземпляров")

    # не больше 3 книг у одного читателя
    active_borrows = db.query(Borrow).filter(
        Borrow.reader_id == reader.id,
        Borrow.returned_at.is_(None)
    ).count()

    if active_borrows >= 3:
        raise HTTPException(status_code=400, detail="Читатель уже взял 3 книги")

    # выдаём книгу
    book.copies_available -= 1
    borrow = Borrow(book_id=book.id, reader_id=reader.id)
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow

@router.post("/return", response_model=BorrowInfo)
def return_book(
    return_data: ReturnRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    borrow = db.query(Borrow).filter(Borrow.id == return_data.borrow_id).first()


    if not borrow:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if borrow.returned_at:
        raise HTTPException(status_code=400, detail="Книга уже возвращена")

    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    if book:
        book.copies_available += 1

    borrow.returned_at = datetime.utcnow()
    db.commit()
    db.refresh(borrow)
    return borrow

# получение списка книг, которые были взяты в аренду у опредленного читателя
@router.get("/reader/{reader_id}/borrowed", response_model=List[BorrowInfo])
def get_borrowed_books(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_db),
):
    return db.query(Borrow).filter(
        Borrow.reader_id == reader_id,
        Borrow.returned_at.is_(None)
    ).all()