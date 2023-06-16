from typing import List

from fastapi import APIRouter, Path, status, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository.search import find_image_by_tag
from src.routes.tags import access_get, access_delete, access_create
from src.schemas.image_schemas import ImageDb
from src.schemas.transformed_image_schemas import TransformedImageResponse
from src.services.auth import auth_service
from src.repository.search import get_img_by_user_id

router = APIRouter(prefix="/search", tags=["Search and filter"])


@router.get("/image/{user_id}", response_model=list[ImageDb],
            dependencies=[Depends(access_get)])
async def get_image_by_user_id(user_id: int = Path(ge=1),
                               db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    images = await get_img_by_user_id(user_id, db, current_user)
    return images


@router.get("/", response_model=List[ImageDb], dependencies=[Depends(access_get)])
async def search_images_by_tag(skip: int = 0, limit: int = 10,
                               search_tag: str = "",
                               filter_type: str = 'd',
                               db: Session = Depends(get_db),
                               user: User = Depends(auth_service.get_current_user)):
    images = await find_image_by_tag(skip, limit, search_tag, filter_type, db, user)
    return images
