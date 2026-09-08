from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    total_copies: int = 1


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int
    available_copies: int

    model_config = {"from_attributes": True}


class LoanCreate(BaseModel):
    book_id: int
    borrower_name: str
    due_date: datetime


class LoanOut(BaseModel):
    id: int
    book_id: int
    borrower_name: str
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    returned: bool

    model_config = {"from_attributes": True}
