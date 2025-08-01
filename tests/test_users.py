import pytest
from fastapi.testclient import TestClient
from app import models
import jwt
from app.config import settings


def test_register_user(client: TestClient):
    response = client.post(
        "/users/register",
        json={
            "name": "nani",
            "email": "nani@gmail.com",
            "password": "nani",
        },
    )
    new_user = models.UserPublic.model_validate(response.json())
    assert new_user.email == "nani@gmail.com"
    assert response.status_code == 200


def test_register_user_existing_email(client: TestClient, test_user1):

    response = client.post(
        "/users/register",
        json={
            "name": "lalz",
            "email": test_user1.email,  # Use the email from the test user
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_login_user(client: TestClient, test_user1):
    # print("new_user:", test_user1)
    response = client.post(
        "/token",
        data={"username": "lalz@gmail.com", "password": "lalz"},
    )
    login_res = models.Token.model_validate(response.json())
    assert login_res.access_token is not None
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, expected_status",
    [
        ("wrongemail@gmail.com", "password123", 401),
        ("lalz@gmail.com", "wrongpassword", 401),
        ("worngemail@gmail.com", "wrongpassword", 401),
        (None, "password123", 401),  # Missing email
        ("lalz@gmail.com", None, 401),  # Missing password
    ],
)
def test_login_user_invalid_credentials(
    client: TestClient, email, password, expected_status
):
    response = client.post(
        "/token",
        data={"username": email, "password": password},
    )
    assert response.status_code == expected_status
