from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BorrowRequest(BaseModel):
    book_id: int
    reader_id: str

class ReturnRequest(BaseModel):
    book_id: int

class BorrowInfo(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrowed_at: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True