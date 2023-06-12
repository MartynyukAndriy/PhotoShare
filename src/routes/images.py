import os

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.image_schemas import ImageAddResponse, ImageUpdateModel
from src.repository import images
from src.services.auth import auth_service
from src.services.images import images_service_id_exists, images_service_change_name
from src.services.roles import RolesAccess

load_dotenv()

router = APIRouter(prefix='/images', tags=["images"])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator, Role.user])
access_delete = RolesAccess([Role.admin, Role.moderator, Role.user])


@router.post("/add", response_model=ImageAddResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(access_create)])
async def upload_image(description: str, file: UploadFile = File(), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        secure=True
    )

    public_name = file.filename.split(".")[0]

    correct_public_name = await images_service_change_name(public_name, db)

    file_name = correct_public_name + str(User.username)
    r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShare/{file_name}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoShare/{file_name}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))

    image = await images.add_image(db, description, src_url, correct_public_name, current_user)

    return {"image": image, "detail": "Image was successfully added"}


@router.get("", dependencies=[Depends(access_get)])
async def get_images(db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    user_images = await images.get_images(db, current_user)
    return user_images


@router.get("/{image_id}", dependencies=[Depends(access_get)])
async def get_image(id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    id_exists = await images_service_id_exists(id, db)
    if id_exists:
        user_image = await images.get_image(db, id, current_user)
        return user_image
    else:
        return "Sorry, there is no image with this id"


@router.put("/{image_info.id}", dependencies=[Depends(access_update)])
async def update_image(image_info: ImageUpdateModel, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    id_exists = await images_service_id_exists(image_info.id, db)
    if id_exists:
        user_image = await images.update_image(db, image_info, current_user)
        return {"image": user_image, "detail": "Image was successfully updated"}
    else:
        return "Sorry, there is no image with this id"


@router.delete("/{id}", dependencies=[Depends(access_delete)])
async def delete_image(id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    id_exists = await images_service_id_exists(id, db)
    if id_exists:
        user_image = await images.delete_image(db, id, current_user)
        return {"image": user_image, "detail": "Image was successfully deleted"}
    else:
        return "Sorry, there is no image with this id"
