from sqlalchemy.orm import Session
from src.database.models.transformed_image_model import TransformedImage
from fastapi import Depends
from src.database.db import get_db


async def get_all_transformed_images_by_true_image_id(true_img_id: int, db: Session = Depends(get_db)):
    mods_list = db.query(TransformedImage).filter(TransformedImage.true_img_id == true_img_id).all()
    return mods_list


