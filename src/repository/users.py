from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.user_schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    pass
    # """
    # The get_user_by_email function takes in an email and a database session,
    # and returns the user associated with that email. If no such user exists, it returns None.
    #
    # :param email: str: Pass in the email address of the user to be retrieved
    # :param db: Session: Pass the database session to the function
    # :return: The user object with the email address that was passed in
    # """
    # return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    pass
    # """
    # The create_user function creates a new user in the database.
    #
    # :param body: UserModel: Get the data from the request body
    # :param db: Session: Access the database
    # :return: The new user
    # """
    # new_user = User(**body.dict())
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    # return new_user


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
