from typing import List

from fastapi import Request, Depends, HTTPException, status

from src.conf.messages import RolesMessages
from src.database.models.user_model import User, Role
from src.services.auth import auth_service


class RolesAccess:
    def __int__(self, allowed_role: List[Role]):
        self.allowed_roles = allowed_role

    async def __call__(self, request: Request, current_user: User = Depends(auth_service.get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=RolesMessages.operation_forbidden)
