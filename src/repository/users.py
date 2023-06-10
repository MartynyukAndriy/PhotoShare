import logging

from sqlalchemy.orm import Session

from src.database.models.users_model import User
from src.schemas.user_schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists, it returns None.

    :param email: str: Pass the email address of the user to be retrieved
    :param db: Session: Pass in a database session
    :return: A user object or none
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        If there are no users with admin role, then the new user will be created as an admin.
        Otherwise, it will be created as a regular user.

    :param body: UserModel: Create a new user object
    :param db: Session: Access the database
    :return: A user object
    """
    admin_exists = db.query(User).filter(User.role == 'admin').first()

    if admin_exists:
        new_user = User(**body.dict(), role='user')
    else:
        new_user = User(**body.dict(),  role='admin')

    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Get the user object from the database
    :param token: str | None: Set the refresh_token field in the user model
    :param db: Session: Commit the changes to the database
    :return: None, so it's not a coroutine
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Get the user's email
    :param db: Session: Access the database
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
