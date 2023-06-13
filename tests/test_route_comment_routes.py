from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime

import pytest

from src.database.models import User, Image
from src.services.auth import auth_service

from src.repository.ratings import get_image

COMMENT = {"comment": "test_comment",
           "user_id": 1,
           "image_id": 1,
           "created_at": str(datetime(year=2012, month=12, day=12)),
           "updated_at": str(datetime(year=2012, month=12, day=12))}


UPDATED_COMMENT = {"comment": "updated_test_comment",
           "user_id": 1,
           "image_id": 1,
           "created_at": str(datetime(year=2012, month=12, day=12)),
           "updated_at": str(datetime(year=2012, month=12, day=12))}


UPDATED_COMMENT_ANOTHER_USER = {"comment": "not your comment",
           "user_id": 2,
           "image_id": 3,
           "created_at": str(datetime(year=2012, month=12, day=12)),
           "updated_at": str(datetime(year=2012, month=12, day=12))}


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_create_comment(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.post(
            "/api/comments",
            json=COMMENT,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["comment"] == COMMENT["comment"]


def test_get_rating(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/comments/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["comment"] == COMMENT["comment"]


def test_get_rating_not_found(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/comments/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "No such comment"


def test_get_comments(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/comments",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["comment"] == COMMENT["comment"]


def test_update_comment(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.put(
            "/api/comments/1",
            json=UPDATED_COMMENT,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["comment"] == UPDATED_COMMENT["comment"]


def test_update_comment_not_found(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.put(
            "/api/comments/2",
            json=UPDATED_COMMENT,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "No such comment"


def test_delete_comment(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.delete(
            "/api/comments/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["comment"] == UPDATED_COMMENT["comment"]



def test_repeat_delete_comment(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.delete(
            "/api/comments/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "No such comment"

