from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.deps import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookOut, BookUpdate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

# создание новой книги
@router.post("/books", response_model=BookOut)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# получение все имеющих книг
@router.get("/books", response_model=List[BookOut])
def get_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Book).all()

# получение одной книги
@router.get("/books/{book_id}", response_model=BookOut)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

# удлаение книги
@router.delete("/books/{book_id}", response_model=BookOut)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    db.delete(book)
    db.commit()

    return book

# обновление данных книги
@router.put("/books/{book_id}", response_model=BookOut)
def update_book(
    book_id: int,
    update_data: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book
