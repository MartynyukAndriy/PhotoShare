from typing import Optional, List

from pydantic import BaseModel, Field


class TransformedImageResponse(BaseModel):
    id: int = 1
    transform_image_url: str = ''
    image_id: int = 1

    class Config:
        orm_mode = True


class UrlTransformedImageResponse(BaseModel):
    transform_image_url: str = ''

    class Config:
        orm_mode = True


class ResizeCropImageFeature(BaseModel):
    fill: bool = Field(default=True)
    crop: bool = Field(default=False)
    thumb: bool = Field(default=False)
    scale: bool = Field(default=False)
    fit: bool = Field(default=False)
    pad: bool = Field(default=False)


class TransformImageCropModel(BaseModel):
    width: int = Field(ge=0, default=300)
    height: int = Field(ge=0, default=300)
    crop: Optional[ResizeCropImageFeature]
    gravity: str = 'auto'


class RadiusImageModel(BaseModel):
    all: int = Field(ge=0, default=0)
    left_top: int = Field(ge=0, default=0)
    right_top: int = Field(ge=0, default=0)
    right_bottom: int = Field(ge=0, default=0)
    left_bottom: int = Field(ge=0, default=0)
    max: bool = Field(default=False)


class RotateImageModel(BaseModel):
    degree: int = Field(ge=-360, le=360, default=0)


class TransformedImageModel(BaseModel):
    resize: Optional[TransformImageCropModel]
    rotate: Optional[RotateImageModel]
    radius: Optional[RadiusImageModel]
