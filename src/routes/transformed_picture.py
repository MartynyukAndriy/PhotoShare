from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, status, Query, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db

from src.schemas.transformed_picture_schemas import TransformPictureModel, TransformPictureResponce
from src.repository import transformed_picture

router = APIRouter(prefix="/pictures", tags=["Transformed pictures"])


@router.get("{true_img_id}/", response_model=List[TransformPictureResponce])
async def get_transformed_pictures(
        true_img_id: int = Path(ge=1),
        db: Session = Depends(get_db)):
    images = await transformed_picture.get_all_transformed_imgs_by_true_image_id(true_img_id, db)
    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Picture with requested parameters not found")
    return images
