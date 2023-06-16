from typing import List

from fastapi import APIRouter, Path, status, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository.search import find_image_by_tag
from src.routes.tags import access_get, access_delete, access_create
from src.schemas.transformed_image_schemas import TransformedImageModel, TransformedImageResponse, \
    UrlTransformedImageResponse
from src.repository.transformed_images import get_all_transformed_images, delete_transformed_image_by_id, \
    create_transformed_picture, get_qrcode_transformed_image_by_id, get_transformed_img_by_id, \
    get_transformed_img_by_user_id, get_url_transformed_image_by_id
from src.services.auth import auth_service

router = APIRouter(prefix="/search", tags=["Search and filter"])


@router.get("/", response_model=List[TransformedImageResponse], dependencies=[Depends(access_get)])
async def search_images_by_tag(skip: int = 0, limit: int = 10,
                               search_tag: str = "",
                               filter_type: int = 1,
                               db: Session = Depends(get_db),
                               user: User = Depends(auth_service.get_current_user)):
    images = await find_image_by_tag(skip, limit, search_tag, filter_type, db, user)
    return images
