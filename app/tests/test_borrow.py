import pytest

# получает jwt токен авторизации
def get_auth_token(client):
    response = client.post("/auth/login", data={
        "username": "user@test.com",
        "password": "password"
    })
    assert response.status_code == 200
    return response.json()["access_token"]

# фикстура возвращает заголовок авторизации
@pytest.fixture(scope="module")
def auth_header(client):
    token = get_auth_token(client)
    return {"Authorization": f"Bearer {token}"}

# тест проверяет, что читатель не может взять больше 3 книг
def test_borrow_limit(client, auth_header):
    for _ in range(3):
        response = client.post("/borrow", headers=auth_header, json={
            "book_id": 1,
            "reader_id": 1
        })
        assert response.status_code == 200

    response = client.post("/borrow", headers=auth_header, json={
        "book_id": 2,
        "reader_id": 1
    })
    assert response.status_code == 400
    assert "3 книги" in response.json()["detail"]

# тест проверяет, что книгу с нулевым количеством экземпляров нельзя выдать
def test_borrow_no_copies(client, auth_header):
    response = client.post("/borrow", headers=auth_header, json={
        "book_id": 3,
        "reader_id": 2
    })
    assert response.status_code == 400
    assert "Нет доступных экземпляров" in response.json()["detail"]

# тест проверяет, что одну и ту же книгу нельзя вернуть дважды
def test_double_return(client, auth_header):
    response = client.post("/borrow", headers=auth_header, json={
        "book_id": 2,
        "reader_id": 2
    })
    assert response.status_code == 200
    borrow_id = response.json()["id"]

    response = client.post("/return", headers=auth_header, json={
        "borrow_id": borrow_id
    })
    assert response.status_code == 200

    response = client.post("/return", headers=auth_header, json={
        "borrow_id": borrow_id
    })
    assert response.status_code == 400
    assert "уже возвращена" in response.json()["detail"]
