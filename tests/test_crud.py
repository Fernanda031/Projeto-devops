import pytest
from datetime import datetime, timedelta

from app import crud, schemas


def test_create_book(db_session):
    book_in = schemas.BookCreate(
        title="Dom Casmurro", author="Machado de Assis", isbn="111", total_copies=2
    )
    book = crud.create_book(db_session, book_in)

    assert book.id is not None
    assert book.available_copies == 2


def test_create_loan_reduces_available_copies(db_session):
    book_in = schemas.BookCreate(
        title="O Cortiço", author="Aluísio Azevedo", isbn="222", total_copies=1
    )
    book = crud.create_book(db_session, book_in)

    loan_in = schemas.LoanCreate(
        book_id=book.id,
        borrower_name="Ana",
        due_date=datetime.utcnow() + timedelta(days=7),
    )
    loan = crud.create_loan(db_session, loan_in)

    updated_book = crud.get_book(db_session, book.id)
    assert loan.returned is False
    assert updated_book.available_copies == 0


def test_create_loan_fails_without_available_copies(db_session):
    book_in = schemas.BookCreate(
        title="Iracema", author="José de Alencar", isbn="333", total_copies=1
    )
    book = crud.create_book(db_session, book_in)
    loan_in = schemas.LoanCreate(
        book_id=book.id,
        borrower_name="Bia",
        due_date=datetime.utcnow() + timedelta(days=7),
    )
    crud.create_loan(db_session, loan_in)

    with pytest.raises(ValueError):
        crud.create_loan(db_session, loan_in)


def test_return_loan_restores_available_copies(db_session):
    book_in = schemas.BookCreate(
        title="Memórias Póstumas", author="Machado de Assis", isbn="444", total_copies=1
    )
    book = crud.create_book(db_session, book_in)
    loan_in = schemas.LoanCreate(
        book_id=book.id,
        borrower_name="Caio",
        due_date=datetime.utcnow() + timedelta(days=7),
    )
    loan = crud.create_loan(db_session, loan_in)

    returned_loan = crud.return_loan(db_session, loan.id)
    updated_book = crud.get_book(db_session, book.id)

    assert returned_loan.returned is True
    assert updated_book.available_copies == 1


def test_return_loan_twice_raises_error(db_session):
    book_in = schemas.BookCreate(
        title="Vidas Secas", author="Graciliano Ramos", isbn="555", total_copies=1
    )
    book = crud.create_book(db_session, book_in)
    loan_in = schemas.LoanCreate(
        book_id=book.id,
        borrower_name="Duda",
        due_date=datetime.utcnow() + timedelta(days=7),
    )
    loan = crud.create_loan(db_session, loan_in)
    crud.return_loan(db_session, loan.id)

    with pytest.raises(ValueError):
        crud.return_loan(db_session, loan.id)
