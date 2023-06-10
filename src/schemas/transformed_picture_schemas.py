from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from src.database.models import Picture, TransformedPicture


class TransformPictureModel(BaseModel):
    true_img_id: int = 1
    transform_img_url: HttpUrl


class TransformPictureResponce(BaseModel):
    id: int = 1
    true_img_id: int = 1
    transform_img_url: HttpUrl

    class Config:
        orm_mode = True
