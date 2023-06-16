from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.schema import datetime

from src.schemas.tag_schemas import TagResponse
from src.schemas.user_schemas import UserResponse


class CommentResponse(BaseModel):
    id: int = 1
    comment: str = 'My comment'

    class Config:
        orm_mode = True


class ImageAddModel(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[str]]


class ImageAddTagModel(BaseModel):
    tags: Optional[List[str]]


class ImageUpdateModel(BaseModel):
    description: str = Field(max_length=500)


class ImageDb(BaseModel):
    id: int
    url: str
    description: str
    tags: List[TagResponse]
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        exclude = {'updated_at', 'user', 'public_name'}


class ImageAdminDb(BaseModel):
    id: int
    url: str
    description: str
    tags: List[TagResponse]
    user: UserResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        exclude = {'public_name', 'user_id'}


class ImageGetResponse(BaseModel):
    image: ImageDb
    ratings: float
    comments: List[CommentResponse]


class ImageAdminGetResponse(BaseModel):
    image: ImageAdminDb
    ratings: float
    comments: List[CommentResponse]


class ImageGetAllResponse(BaseModel):
    images: List[ImageGetResponse]


class ImageAdminGetAllResponse(BaseModel):
    images: List[ImageAdminGetResponse]


class ImageAddResponse(BaseModel):
    image: ImageDb
    detail: str = "Image was successfully added"

    class Config:
        orm_mode = True


class ImageAddTagResponse(BaseModel):
    id: int
    tags: List[TagResponse]
    detail: str = "Image was successfully updated"

    class Config:
        orm_mode = True


class ImageUpdateDescrResponse(BaseModel):
    id: int
    description: str
    detail: str = "Image was successfully updated"

    class Config:
        orm_mode = True


class ImageDeleteResponse(BaseModel):
    image: ImageDb
    detail: str = "Image was successfully deleted"
