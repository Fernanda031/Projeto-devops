from datetime import datetime
from sqlalchemy.orm import Session

from app import models, schemas


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        total_copies=book.total_copies,
        available_copies=book.total_copies,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session):
    return db.query(models.Book).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def search_books(db: Session, title: str = None, author: str = None):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    return query.all()
    
def create_loan(db: Session, loan: schemas.LoanCreate) -> models.Loan:
    book = get_book(db, loan.book_id)
    if book is None:
        raise ValueError("Livro não encontrado")
    if book.available_copies <= 0:
        raise ValueError("Não há exemplares disponíveis para empréstimo")

    book.available_copies -= 1
    db_loan = models.Loan(
        book_id=loan.book_id,
        borrower_name=loan.borrower_name,
        due_date=loan.due_date,
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def return_loan(db: Session, loan_id: int) -> models.Loan:
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if loan is None:
        raise ValueError("Empréstimo não encontrado")
    if loan.returned:
        raise ValueError("Este livro já foi devolvido")

    loan.returned = True
    loan.return_date = datetime.utcnow()

    book = get_book(db, loan.book_id)
    if book is not None:
        book.available_copies += 1

    db.commit()
    db.refresh(loan)
    return loan
