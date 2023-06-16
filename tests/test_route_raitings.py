from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime

import pytest

from src.database.models import User, Image
from src.services.auth import auth_service

from src.repository.ratings import get_image

RATING = {
           "one_star": False,
            "two_stars": True,
            "three_stars": False,
            "four_stars": False,
            "five_stars": False}

UPDATED_RATING = {
           "one_star": False,
            "two_stars": False,
            "three_stars": True,
            "four_stars": False,
            "five_stars": False}

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

def test_create_rating_success(client, token):
    fake_image = Image(url="test_url", description="test_description", public_name="test_name", user_id=2, created_at=datetime(year=2012, month=12, day=12), updated_at=datetime(year=2012, month=12, day=12))
    with patch("src.repository.ratings.get_image", return_value=fake_image):
        response = client.post("api/ratings/1", json=RATING, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        rating = response.json()
        assert rating["one_star"] == RATING["one_star"]

def test_create_rating_for_own_image(client, token):
    fake_image = Image(url="test_url", description="test_description", public_name="test_name", user_id=1, created_at=datetime(year=2012, month=12, day=12), updated_at=datetime(year=2012, month=12, day=12))
    with patch("src.repository.ratings.get_image", return_value=fake_image):
        response = client.post("api/ratings/1", json=RATING, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Please, check the image_id. You can't rate your images or give 2 or more rates for 1 image"



def test_get_ratings(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/ratings/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["one_star"] == RATING["one_star"]


def test_get_rating_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/ratings/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Rating not found"


def test_common_image_rating(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/ratings/image/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["average_rating"] == 0.0


def test_update_rating(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/ratings/1",
            json=UPDATED_RATING,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["one_star"] == RATING["one_star"]


def test_update_tag_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/ratings/2",
            json=UPDATED_RATING,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Rating not found or you can't update the rating because of rules or roles"


def test_delete_tag(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/ratings/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["one_star"] == RATING["one_star"]



def test_repeat_delete_tag(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/ratings/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Rating not found or you don't have enough rules to delete"
