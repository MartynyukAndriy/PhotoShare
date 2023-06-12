from pydantic import BaseModel
from pydantic.schema import datetime


class ImageUpdateModel(BaseModel):
    id: int
    description: str


class ImageDb(BaseModel):
    id: int
    url: str
    description: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ImageAddResponse(BaseModel):
    image: ImageDb
    detail: str = "Image was successfully added"





