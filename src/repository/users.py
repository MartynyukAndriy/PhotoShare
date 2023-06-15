from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import User
from src.schemas.user_schemas import UserModel, UserUpdate, UserBlackList


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

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user that is being updated
    :param token: str | None: Pass in the token that is returned from the api
    :param db: Session: Access the database
    :return: Nothing
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.

    :param email: str: Pass the email of the user to be confirmed
    :param db: Session: Pass the database session to the function
    :return: Nothing
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def get_user_info(username: str, db: Session):

    """
    The get_user_info function takes in a username and returns the user's information.
        Args:
            username (str): The name of the user to be retrieved from the database.
    :param username: str: Specify the username of the user
    :param db: Session: Pass the database session to the function
    :return: A dictionary of the user's information
    """
    user = db.query(User).filter(User.username == username).first()
    return user


async def update_user_info(body: UserUpdate, username: str, db: Session):
    """
    Update the user information with the provided updated fields based on the username.
    :param body: UserUpdate: Updated fields for the user
    :param username: str: User's username
    :param db: Session: Access the database
    :return: Updated user object
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.username = body.username
    user.email = body.email
    db.commit()
    return user


async def block(email: str, body: UserBlackList, db: Session):
    """Description"""
    user = await get_user_by_email(email, db)
    if user:
        user.banned = body.banned
        db.commit()
    return user
