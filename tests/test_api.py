from datetime import datetime, timedelta


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_list_books(client):
    response = client.post(
        "/books",
        json={
            "title": "1984",
            "author": "George Orwell",
            "isbn": "999",
            "total_copies": 3,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["available_copies"] == 3

    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_loan_flow_end_to_end(client):
    book_resp = client.post(
        "/books",
        json={
            "title": "Fahrenheit 451",
            "author": "Ray Bradbury",
            "isbn": "888",
            "total_copies": 1,
        },
    )
    book_id = book_resp.json()["id"]

    due_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
    loan_resp = client.post(
        "/loans",
        json={"book_id": book_id, "borrower_name": "Elis", "due_date": due_date},
    )
    assert loan_resp.status_code == 200
    loan_id = loan_resp.json()["id"]

    book_after_loan = client.get(f"/books/{book_id}").json()
    assert book_after_loan["available_copies"] == 0

    return_resp = client.post(f"/loans/{loan_id}/return")
    assert return_resp.status_code == 200
    assert return_resp.json()["returned"] is True

    book_after_return = client.get(f"/books/{book_id}").json()
    assert book_after_return["available_copies"] == 1


def test_get_nonexistent_book_returns_404(client):
    response = client.get("/books/999")
    assert response.status_code == 404

def test_search_books_by_title(client):
    client.post("/books", json={"title": "Capitu", "author": "Machado", "isbn": "777", "total_copies": 1})
    response = client.get("/books/search?title=Capitu")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_create_book_with_duplicate_isbn_fails(client):
    client.post(
        "/books",
        json={"title": "Livro A", "author": "Autor A", "isbn": "555", "total_copies": 1},
    )
    response = client.post(
        "/books",
        json={"title": "Livro B", "author": "Autor B", "isbn": "555", "total_copies": 1},
    )
    assert response.status_code >= 400


def test_create_loan_for_nonexistent_book_fails(client):
    from datetime import datetime, timedelta

    due_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
    response = client.post(
        "/loans",
        json={"book_id": 9999, "borrower_name": "Alguém", "due_date": due_date},
    )
    assert response.status_code == 400


def test_return_loan_twice_via_api_fails(client):
    from datetime import datetime, timedelta

    book_resp = client.post(
        "/books",
        json={"title": "Livro C", "author": "Autor C", "isbn": "666", "total_copies": 1},
    )
    book_id = book_resp.json()["id"]

    due_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
    loan_resp = client.post(
        "/loans",
        json={"book_id": book_id, "borrower_name": "Fê", "due_date": due_date},
    )
    loan_id = loan_resp.json()["id"]

    client.post(f"/loans/{loan_id}/return")
    second_return = client.post(f"/loans/{loan_id}/return")
    assert second_return.status_code == 400