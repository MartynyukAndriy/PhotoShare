from pydantic import BaseModel, EmailStr, Field

from src.database.models.users_model import Role


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str
    role: Role

    class Config:
        orm_mode = True
