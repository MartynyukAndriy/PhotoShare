from typing import List

from fastapi import APIRouter, Path, status, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.transformed_image_schemas import TransformedImageModel, TransformedImageResponse, \
    UrlTransformedImageResponse
from src.repository.transformed_images import get_all_transformed_images, delete_transformed_image_by_id, \
    create_transformed_picture, get_qrcode_transformed_image_by_id, get_transformed_image_by_id

router = APIRouter(prefix="/transformed_images", tags=["Transformed images"])


@router.post("/{image_id}", response_model=TransformedImageResponse, status_code=status.HTTP_201_CREATED)
async def create_new_transformed_image(body: TransformedImageModel, image_id: int = Path(ge=1),
                                       db: Session = Depends(get_db)):
    new_transformed_picture = await create_transformed_picture(body, image_id, db)
    return new_transformed_picture


@router.get("/{image_id}", response_model=List[TransformedImageResponse])
async def get_all_transformed_images_for_original_image_by_id(skip: int = 0, limit: int = 10,
                                                              image_id: int = Path(ge=1),
                                                              db: Session = Depends(get_db)):
    images = await get_all_transformed_images(skip, limit, image_id, db)
    return images


@router.get("/transformed/{transformed_image_id}", response_model=TransformedImageResponse)
async def get_transformed_pictures(transformed_image_id: int = Path(ge=1),
                                   db: Session = Depends(get_db)):
    transformed_image = await get_transformed_image_by_id(transformed_image_id, db)
    return transformed_image


@router.get("/transformed/{transformed_image_id}/qrcode", response_model=UrlTransformedImageResponse)
async def get_qrcode_for_transformed_pictures(transformed_image_id: int = Path(ge=1),
                                              db: Session = Depends(get_db)):
    transformed_image = await get_qrcode_transformed_image_by_id(transformed_image_id, db)
    return ''


@router.delete("/transformed/{transformed_image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transformed_image(transformed_image_id: int = Path(ge=1),
                                   db: Session = Depends(get_db)):
    transformed_image = await delete_transformed_image_by_id(transformed_image_id, db)
    return None
