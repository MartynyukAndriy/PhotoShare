from fastapi import APIRouter, Depends

from src.database.models.user_model import Role, User
from src.services.roles import RolesAccess
from src.schemas.user_schemas import UserResponse
from src.services.auth import auth_service

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator, Role.user])
access_delete = RolesAccess([Role.admin])

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET request that returns the current user's information.
        It requires authentication, and it uses the auth_service to get the current user.

    :param current_user: User: Pass the current user object to the function
    :return: The current user object, which is obtained from the auth_service
    """
    return current_user
