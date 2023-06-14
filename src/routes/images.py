import os

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.image_schemas import ImageAddResponse, ImageUpdateModel, ImageAddModel, ImageAddTagResponse, \
    ImageAddTagModel, ImageGetAllResponse, ImageGetResponse, ImageDeleteResponse, ImageUpdateDescrResponse, \
    ImageAdminGetAllResponse
from src.repository import images
from src.services.auth import auth_service
from src.services.images import images_service_change_name, normalize_tags
from src.services.roles import RolesAccess

load_dotenv()

router = APIRouter(prefix='/images', tags=["images"])

access_all = RolesAccess([Role.admin, Role.moderator, Role.user])
access_admin = RolesAccess([Role.admin])


@router.get("", response_model=ImageGetAllResponse, dependencies=[Depends(access_all)])
async def get_images(db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    user_images = await images.get_images(db, current_user)
    return {"images": user_images}


@router.get("/image_id/{id}", response_model=ImageGetResponse, dependencies=[Depends(access_all)])
async def get_image(id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    print('Usual GET')
    user_image, ratings, comments = await images.get_image(db, id, current_user)
    return {"image": user_image, "ratings": ratings, "comments": comments}


@router.get("/user_id/{user_id}", response_model=ImageAdminGetAllResponse, dependencies=[Depends(access_admin)])
async def admin_get_images(user_id: int, db: Session = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):
    print("Started")
    user_response = await images.admin_get_image(db, user_id)
    return {"images": user_response}


@router.post("/add", response_model=ImageAddResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(access_all)])
async def upload_image(body: ImageAddModel = Depends(), file: UploadFile = File(), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        secure=True
    )

    correct_tags = await normalize_tags(body)

    public_name = file.filename.split(".")[0]

    correct_public_name = await images_service_change_name(public_name, db)

    file_name = correct_public_name + "_" + str(current_user.username)
    r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShare/{file_name}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoShare/{file_name}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))

    image = await images.add_image(db, body, correct_tags, src_url, correct_public_name, current_user)

    return {"image": image, "detail": "Image was successfully added"}


@router.put("/update_description/{image_id}", response_model=ImageUpdateDescrResponse,
            dependencies=[Depends(access_all)])
async def update_description(image_id: int, image_info: ImageUpdateModel, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    user_image = await images.update_image(db, image_id, image_info, current_user)
    return {"id": user_image.id, "description": user_image.description, "detail": "Image was successfully updated"}


@router.put("/update_tags/{image_id}", response_model=ImageAddTagResponse, dependencies=[Depends(access_all)])
async def add_tag(image_id, body: ImageAddTagModel = Depends(), db: Session = Depends(get_db),
                  current_user: User = Depends(auth_service.get_current_user)):
    image = await images.add_tag(db, image_id, body, current_user)
    return {"id": image.id, "tags": image.tags, "detail": "Image was successfully updated"}


@router.delete("/{id}", response_model=ImageDeleteResponse, dependencies=[Depends(access_all)])
async def delete_image(id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    await images_service_id_exists(id, db)
    user_image = await images.delete_image(db, id, current_user)
    return {"image": user_image, "detail": "Image was successfully deleted"}
