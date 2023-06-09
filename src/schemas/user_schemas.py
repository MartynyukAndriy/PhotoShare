from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    pass
    # username: str = Field(min_length=5, max_length=16)
    # email: EmailStr
    # password: str = Field(min_length=6, max_length=10)


class UserResponse(BaseModel):
    pass
    # id: int
    # username: str
    # email: EmailStr
    # avatar: str

    class Config:
        orm_mode = True
