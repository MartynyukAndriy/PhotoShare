from pydantic import BaseModel
from pydantic.schema import datetime


class ImageAddModel(BaseModel):
    description: str


class ImageUpdateModel(BaseModel):
    id: int
    description: str


class ImageDb(BaseModel):
    id: int
    url: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ImageAddResponse(BaseModel):
    image: ImageDb
    detail: str = "Image was successfully added"


class ImageUpdateResponse(BaseModel):
    image: ImageDb
    detail: str = "Image was successfully updated"


class ImageDeleteResponse(BaseModel):
    image: ImageDb
    detail: str = "Image was successfully deleted"