# Додавання ролей

from src.database.roles import Role
from src.services.roles import RolesAccess

access_get = RolesAccess([Role.administrator, Role.moderator, Role.user])
access_create = RolesAccess([Role.administrator, Role.moderator, Role.user])
access_update = RolesAccess([Role.administrator, Role.moderator, Role.user])
access_delete = RolesAccess([Role.administrator])

# Приклад
@router.get("/me/", response_model=UserResponse, dependencies=[Depends(access_get)]) # Оцю фігню dependencies=[Depends(access_get) додавати до кожного роута, відповідно до операції
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user