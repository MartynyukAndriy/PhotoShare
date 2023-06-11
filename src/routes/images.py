import os

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.database.db import get_db
from src.schemas.image_schemas import ImageAddResponse, ImageDb, ImageUpdateResponse, ImageUpdateModel, \
    ImageDeleteResponse
from src.repository import images

load_dotenv()

router = APIRouter(prefix='/images', tags=["images"])


@router.post("/add", response_model=ImageAddResponse)
async def upload_image(description: str, file: UploadFile = File(), db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        secure=True
    )

    public_name = file.filename.split(".")[0]

    r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShare/{description}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoShare/{description}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))

    image = await images.add_image(db, description, src_url, public_name)

    return {"image": image, "detail": "Image was successfully added"}


@router.get("/{image_id}", response_model=ImageDb)
async def get_image(id: int, db: Session = Depends(get_db)):
    user_image = await images.get_image(db, id)
    return user_image


@router.put("/{image_info.id}", response_model=ImageUpdateResponse)
async def update_image(image_info: ImageUpdateModel, db: Session = Depends(get_db)):
    user_image = await images.update_image(db, image_info)
    return {"image": user_image, "detail": "Image was successfully updated"}


@router.delete("/{id}", response_model=ImageDeleteResponse)
async def delete_image(id: int, db: Session = Depends(get_db)):
    user_image = await images.delete_image(db, id)
    return {"image": user_image, "detail": "Image was successfully deleted"}
