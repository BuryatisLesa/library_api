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
# выдача книг
@router.post("/borrow", response_model=BorrowInfo)
def borrow_book(
    borrow_data: BorrowRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == borrow_data.book_id).first()
    reader = db.query(Reader).filter(Reader.id == borrow_data.reader_id).first()

    if not book and not reader:
        raise HTTPException(status_code=404, detail="Книга или читатель не найдены")
    
    borrow = Borrow(book_id = book.id, reader_id = reader.id)

    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow

# возвращение книги
@router.post("/borrow", response_model=BorrowInfo)
def return_book(
    return_data: ReturnRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    borrow = db.query(Borrow).filter(Borrow.id == return_data.book_id).first()

    if not borrow or borrow.returned_at is not None:
        raise HTTPException(status_code=404, detail="Выдача не найдена или уже возвращена")
    

    borrow.returned_at = datetime.utcnow()
    db.commit()
    db.refresh(borrow)
    return borrow

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