import pytest
from sqlalchemy.orm import Session

from src.database.models import User
from src.repository.users import get_user_by_email, update_token, confirmed_email, get_user_info, update_user_info


@pytest.mark.asyncio
async def test_get_user_by_email(session: Session):
    """
    The test_get_user_by_email function tests the get_user_by_email function in the users.py file.
    It creates a user with an email address, adds it to the database, and then calls get_user_by_email
    with that same email address as an argument. It asserts that this call returns a User object and
    that its email attribute is equal to what was passed into get user by email.
    :param session: Session: Pass in a database session to the function
    :return: The user object with the email address that was passed in
    """
    email = "test@example.com"
    user = User(username="testuser", email=email, password="password")
    session.add(user)
    session.commit()

    result = await get_user_by_email(email, session)

    assert result is not None
    assert result.email == email


@pytest.mark.asyncio
async def test_update_token(session: Session):
    """
    The test_update_token function tests the update_token function.
    It does this by creating a user, adding it to the database, and then calling update_token with that user.
    The test passes if the refresh token of that user is equal to &quot;new_token&quot;.
    :param session: Session: Pass in a database session to the function
    :return: None
    """
    user = User(username="testuser", email="test@example.com", password="password")
    session.add(user)
    session.commit()
    token = "new_token"

    await update_token(user, token, session)

    session.refresh(user)
    assert user.refresh_token == token


@pytest.mark.asyncio
async def test_confirmed_email(session: Session):
    """
    The test_confirmed_email function tests the confirmed_email function.
    It creates a user with an email address and sets their confirmed field to False.
    Then it calls the confirmed_email function, passing in that email address and session object.
    Finally, it checks that the user's confirmed field is now True.
    :param session: Session: Pass a database session to the function
    :return: A boolean value, which is true if the user's email has been confirmed
    """
    email = "test@example.com"
    user = User(username="testuser", email=email, password="password", confirmed=False)
    session.add(user)
    session.commit()

    await confirmed_email(email, session)

    confirmed_user = await get_user_by_email(email, session)
    assert confirmed_user.confirmed is True


@pytest.mark.asyncio
async def test_get_user_info(session: Session):
    """
    The test_get_user_info function tests the get_user_info function.
    It does this by creating a user in the database, then calling get_user_info with that username.
    The test passes if it gets back a User object with the same username and email as what was created.
    :param session: Session: Pass in a database session
    :return: An object containing the user's information
    """
    username = "testuser"
    user = User(username=username, email="test@example.com", password="password")
    session.add(user)
    session.commit()

    user_info = await get_user_info(username, session)

    assert user_info is not None
    assert user_info.username == username
    assert user_info.email == "test@example.com"


@pytest.mark.asyncio
async def test_update_user_info(session: Session):
    """
    The test_update_user_info function tests the update_user_info function.
        Args:
            session (Session): The database session to use for this test.
    :param session: Session: Create a database session for the test
    :return: The updated user
    """
    username = "testuser"
    user = User(username=username, email="test@example.com", password="password")
    session.add(user)
    session.commit()

    updated_username = "newuser"
    updated_email = "new@example.com"
    updated_body = User(username=updated_username, email=updated_email)

    # Act
    updated_user = await update_user_info(updated_body, username, session)

    # Assert
    assert updated_user is not None
    assert updated_user.username == updated_username
    assert updated_user.email == updated_email
