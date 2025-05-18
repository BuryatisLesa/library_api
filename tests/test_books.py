from tests.conftest import client

def test_get_books_unauthorized(client):
    response = client.get("/books")
    assert response.status_code == 401

def test_create_book_unauthorized(client):
    response = client.post("/books", json={"title": "Test", "author": "Author"})
    assert response.status_code == 401