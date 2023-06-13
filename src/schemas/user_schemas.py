from pydantic import BaseModel, EmailStr, Field

from src.database.models import Role


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int
    username: str = "Bob"
    email: EmailStr = "bob@gmail.com"
    role: Role = "user"

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str
    email: EmailStr
