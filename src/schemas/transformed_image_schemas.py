from pydantic import BaseModel


class TransformedImageResponse(BaseModel):
    id: int = 1
    transform_image_url: str = ''
    image_id: int = 1

    class Config:
        orm_mode = True


class TransformedImageModel(BaseModel):
    width: int = 500
    height: int = 500
    crop: str = "fill"
    # effect: str = "grayscale"
    angle: int = 15


class UrlTransformedImageResponse(BaseModel):
    transform_image_url: str = ''
