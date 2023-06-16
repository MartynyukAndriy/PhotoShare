from unittest.mock import MagicMock, patch

import pytest

from src.database.models import User
from src.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    """
    The token function is used to create a user, confirm the user, and then log in as that
    user. It returns the access token for that user.
    :param client: Test the routes
    :param user: Create a user to test the token function
    :param session: Create a new session for the test
    :param monkeypatch: Mock the send_email function in the token function
    :return: A token, which is a string
    """
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


def test_read_users_me_authenticated(client, token):
    """
    The test_read_users_me_authenticated function tests that a user can read their own information.
    It does this by first mocking the redis cache to return None, which will cause the function to hit the database.
    Then it creates a request with an Authorization header containing a valid token and sends it to /api/users/me/.
    The response is checked for status code 200 (OK) and then its JSON data is checked for username, email, but not password.
    :param client: Make requests to the api
    :param token: Pass the token to the test function
    :return: A 200 status code and a user object with the username and email
    """

    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/users/me/", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert "username" in data
        assert "email" in data
        assert "password" not in data


def test_profile_info(client, token):
    """
    The test_profile_info function tests the /api/users/&lt;username&gt; endpoint.
    It does so by first patching the auth_service module's r object to return None,
    then it makes a GET request to /api/users/deadpool/, passing in an Authorization header with a valid token.
    The response is then checked for status code 200 and that it contains &quot;username&quot; and &quot;deadpool&quot;.
    :param client: Send a request to the api server
    :param token: Pass in the token that is generated from the fixture
    :return: A 200 status code and a json object with the username of the user
    """
    with patch.object(auth_service, 'r') as r_mock:
            r_mock.get.return_value = None
            username = "deadpool"
            response = client.get(f"/api/users/{username}/",
                                  headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 200, response.text
            data = response.json()
            assert "username" in data
            assert data["username"] == username


def test_profile_info_user_not_found(client, token):
    """
    The test_profile_info_user_not_found function tests the profile_info endpoint with a username that does not exist.
    It uses the client fixture to make a GET request to /api/users/not_deadpool/, and passes in an Authorization header with
    a valid token. The test then asserts that the response status code is 404, and checks if data[&quot;detail&quot;] == &quot;User not found&quot;.
    :param client: Make a request to the api
    :param token: Pass the token to the test function
    :return: A 404 status code and the detail of the error
    """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        username = "not_deadpool"
        response = client.get(f"/api/users/{username}/",
                              headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "User not found"
