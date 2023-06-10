from typing import List

from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db

from src.schemas.transformed_image_schemas import TransformedImageModel, TransformedImageResponse
from src.repository import transformed_images

router = APIRouter(prefix="/transformed_images", tags=["Transformed images"])


@router.get("/{image_id}/", response_model=List[TransformedImageResponse])
async def get_transformed_pictures(
        true_img_id: int = Path(ge=1),
        db: Session = Depends(get_db)):
    images = await transformed_images.get_all_transformed_images_by_true_image_id(true_img_id, db)
    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Picture with requested parameters not found")
    return images
