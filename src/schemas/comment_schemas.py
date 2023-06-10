from datetime import date

from pydantic import BaseModel, EmailStr, Field


class CommentModel(BaseModel):
    comment: str = Field(min_length=1, max_length=255)
    user_id: int = Field(1, gt=0)
    picture_id: int = Field(1, gt=0)


class CommentResponse(BaseModel):
    id: int = 1
    comment: str = 'My comment'
    user: UserResponse
    picture: PictureResponse

    class Config:
        orm_mode = True