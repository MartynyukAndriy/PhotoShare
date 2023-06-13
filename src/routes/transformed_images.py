from typing import List

from fastapi import APIRouter, Path, status, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.routes.tags import access_get, access_delete, access_create
from src.schemas.transformed_image_schemas import TransformedImageModel, TransformedImageResponse, \
    UrlTransformedImageResponse
from src.repository.transformed_images import get_all_transformed_images, delete_transformed_image_by_id, \
    create_transformed_picture, get_qrcode_transformed_image_by_id, get_transformed_img_by_id, \
    get_transformed_img_by_user_id, get_url_transformed_image_by_id
from src.services.auth import auth_service

router = APIRouter(prefix="/transformed_images", tags=["Transformed images"])


@router.post("/{image_id}", response_model=TransformedImageResponse,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(access_create)])
async def create_new_transformed_image(body: TransformedImageModel,
                                       user: User = Depends(auth_service.get_current_user),
                                       image_id: int = Path(ge=1),
                                       db: Session = Depends(get_db), ):
    new_transformed_picture = await create_transformed_picture(body, user, image_id, db)
    return new_transformed_picture


@router.get("/{image_id}", response_model=List[TransformedImageResponse], dependencies=[Depends(access_get)])
async def get_all_transformed_images_for_original_image_by_id(skip: int = 0, limit: int = 10,
                                                              image_id: int = Path(ge=1),
                                                              db: Session = Depends(get_db),
                                                              user: User = Depends(auth_service.get_current_user)):
    images = await get_all_transformed_images(skip, limit, image_id, db, user)
    return images


@router.get("/transformed/{transformed_image_id}", response_model=TransformedImageResponse,
            dependencies=[Depends(access_get)])
async def get_transformed_images_by_image_id(transformed_image_id: int = Path(ge=1),
                                             db: Session = Depends(get_db),
                                             user: User = Depends(auth_service.get_current_user)):
    transformed_image = await get_transformed_img_by_id(transformed_image_id, db, user)
    return transformed_image


@router.get("/transformed/{transformed_image_id}/qrcode", response_model=UrlTransformedImageResponse,
            dependencies=[Depends(access_get)])
async def get_qrcode_for_transformed_image(transformed_image_id: int = Path(ge=1),
                                           db: Session = Depends(get_db),
                                           user: User = Depends(auth_service.get_current_user)):
    transformed_image = await get_qrcode_transformed_image_by_id(transformed_image_id, db, user)
    return transformed_image


@router.get("/transformed/{transformed_image_id}/url", response_model=UrlTransformedImageResponse,
            dependencies=[Depends(access_get)])
async def get_url_for_transformed_image(transformed_image_id: int = Path(ge=1),
                                        db: Session = Depends(get_db),
                                        user: User = Depends(auth_service.get_current_user)):
    transformed_image = await get_url_transformed_image_by_id(transformed_image_id, db, user)
    return transformed_image


@router.delete("/transformed/{transformed_image_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(access_delete)])
async def delete_transformed_image(transformed_image_id: int = Path(ge=1),
                                   db: Session = Depends(get_db),
                                   user: User = Depends(auth_service.get_current_user)):
    transformed_image = await delete_transformed_image_by_id(transformed_image_id, db, user)
    return None


@router.get("/user/transformed/{user_id}", response_model=list[TransformedImageResponse],
            dependencies=[Depends(access_get)])
async def get_transformed_images_by_user_id(user_id: int = Path(ge=1),
                                            db: Session = Depends(get_db),
                                            current_user: User = Depends(auth_service.get_current_user)):
    transformed_images = await get_transformed_img_by_user_id(user_id, db, current_user)
    return transformed_images
