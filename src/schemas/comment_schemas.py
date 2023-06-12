from pydantic import BaseModel, Field

from src.schemas.image_schemas import ImageAddResponse
from src.schemas.user_schemas import UserResponse


class CommentModel(BaseModel):
    comment: str = Field(min_length=1, max_length=255)
    user_id: int = Field(1, gt=0)
    image_id: int = Field(1, gt=0)


class CommentResponse(BaseModel):
    id: int = 1
    comment: str = 'My comment'
    user: UserResponse
    # image: ImageAddResponse

    class Config:
        orm_mode = True


class CommentDeleteResponse(BaseModel):
    id: int = 1
    comment: str = 'My comment'

    class Config:
        orm_mode = True

