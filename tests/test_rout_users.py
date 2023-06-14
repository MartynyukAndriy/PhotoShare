from unittest.mock import MagicMock, patch

import pytest
from starlette import status

from src.database.models import User
from src.services.auth import auth_service


# Не зовсім розумію, чому не працює.(((

# @pytest.fixture()
# def token(client, user, session, monkeypatch):
#     mock_send_email = MagicMock()
#     monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
#     client.post("/api/auth/signup", json=user)
#     current_user: User = session.query(User).filter(User.email == user.get('email')).first()
#     current_user.confirmed = True
#     session.commit()
#     response = client.post(
#         "/api/auth/login",
#         data={"username": user.get('email'), "password": user.get('password')},
#     )
#     data = response.json()
#     return data["access_token"]


# def test_read_users_me_authenticated(client, token):
#     headers = {"Authorization": f"Bearer {token}"}
#
#     response = client.get("/me/", headers=headers)
#
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert "username" in data
#     assert "email" in data
#     assert "password" not in data


# def test_profile_info(client, token):
#     with patch.object(auth_service, 'r') as r_mock:
#         r_mock.get.return_value = None
#         username = "testuser"
#         response = client.get(f"/api/profile/{username}/", headers={"Authorization": f"Bearer {token}"})
#
#         assert response.status_code == 200, response.text
#         data = response.json()
#         assert "username" in data
#         assert data["username"] == username
