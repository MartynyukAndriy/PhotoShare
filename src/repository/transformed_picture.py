from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.database.models import TransformedPicture
from fastapi import Depends
from src.database.db import get_db


async def get_all_transformed_imgs_by_true_image_id(true_img_id: int, db: Session = Depends(get_db)):
    mods_list = db.query(TransformedPicture).filter(TransformedPicture.true_img_id == true_img_id).all()
    return mods_list


