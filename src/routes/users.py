from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.database.models import User, Role
from src.repository.users import get_user_info, update_user_info, block
from src.schemas.user_schemas import UserResponse, UserUpdate, UserBlackList, UserBlacklistResponse
from src.services.auth import auth_service
from src.services.roles import RolesAccess

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator, Role.user])
access_delete = RolesAccess([Role.admin])
access_block = RolesAccess([Role.admin])

router = APIRouter(prefix="/users", tags=["Users profile"])


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET request that returns the current user's information.
        It requires authentication, and it uses the auth_service to get the current user.

    :param current_user: User: Pass the current user object to the function
    :return: The current user object, which is obtained from the auth_service
    """
    return current_user


@router.get("/{username}/", response_model=UserResponse)
async def profile_info(username: str, db: Session = Depends(get_db)):
    """
    Get information about a user based on their username.
    :param username: str: User's username
    :param db: Session: Access the database
    :return: User object
    """
    user_info = await get_user_info(username, db)
    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info


@router.put('/{username}', response_model=UserResponse, dependencies=[Depends(access_update)])
async def profile_update(username: str, body: UserUpdate, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The profile_update function updates the user's profile information.
        The function takes in a username, body (which is a UserUpdate object), db (a database session), and current_user.
        If the current_user's username does not match the given username and their role is 'user', then an HTTPException
            with status code 403 Forbidden will be raised, along with an error message stating that they can only update
            their own profile. Otherwise, updated_user will be set to await update_user_info(body, username, db). Finally,
            updated user will be returned.
    :param username: str: Get the username of the user to be updated
    :param body: UserUpdate: Get the data from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the current user,
    :return: An updated user object
    """
    if current_user.username != username and current_user.role == 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own profile")

    updated_user = await update_user_info(body, username, db)

    return updated_user


@router.patch("/{email}/blacklist", response_model=UserBlacklistResponse, dependencies=[Depends(access_block)])
async def block_user(email: str, body: UserBlackList, db: Session = Depends(get_db),
                        _: User = Depends(auth_service.get_current_user)):
    """Description"""
    blocked_user = await block(email, body, db)
    if blocked_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return blocked_user
