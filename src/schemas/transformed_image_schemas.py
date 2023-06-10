from pydantic import BaseModel, HttpUrl


class TransformedImageModel(BaseModel):
    image_id: int = 1
    transform_image_url: HttpUrl
    qr_transformed_image: HttpUrl


class TransformedImageResponse(BaseModel):
    id: int = 1
    image: ImageResponse
    transform_image_url: HttpUrl
    qr_transformed_image: HttpUrl

    class Config:
        orm_mode = True
