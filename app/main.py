from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas, crud
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Biblioteca")


@app.get("/")
def root():
    return {"status": "ok", "service": "library-system"}


@app.post("/books", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db, book)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/books", response_model=list[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    return crud.get_books(db)

@app.get("/books/search", response_model=list[schemas.BookOut])
def search_books(title: Optional[str] = None, author: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.search_books(db, title=title, author=author)

@app.get("/books/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book


@app.post("/loans", response_model=schemas.LoanOut)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_loan(db, loan)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/loans/{loan_id}/return", response_model=schemas.LoanOut)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    try:
        return crud.return_loan(db, loan_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
