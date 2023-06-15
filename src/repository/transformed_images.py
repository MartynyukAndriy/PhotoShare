import cloudinary
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import TransformedImage, Image, User
from src.database.db import get_db
from src.schemas.transformed_image_schemas import TransformedImageModel
from src.services.transformed_image import create_qrcode, create_transformations


async def create_transformed_picture(body: TransformedImageModel,
                                     current_user,
                                     image_id: int,
                                     db: Session = Depends(get_db)):
    original_image = db.query(Image).filter(Image.id == image_id and Image.user_id == current_user.id).first()
    if not original_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Original image not found")

    transformations = create_transformations(body)

    public_id = original_image.public_name
    file_name = public_id + "_" + str(current_user.username)
    new_url = cloudinary.CloudinaryImage(f'PhotoShare/{file_name}').build_url(transformation=transformations)

    new_transformed_image = TransformedImage(transform_image_url=new_url, image_id=original_image.id)
    db.add(new_transformed_image)
    db.commit()
    db.refresh(new_transformed_image)
    return new_transformed_image


async def get_all_transformed_images(skip: int, limit: int, image_id: int, db: Session, current_user):
    transformed_list = db.query(TransformedImage).join(Image). \
        filter(TransformedImage.image_id == image_id and Image.user_id == current_user.id). \
        offset(skip).limit(limit).all()
    if not transformed_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed images for this image not found")
    return transformed_list


async def get_transformed_img_by_id(transformed_id: int, db: Session, current_user):
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(TransformedImage.id == transformed_id and Image.user_id == current_user.id).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
    return transformed_image


async def delete_transformed_image_by_id(transformed_id: int, db: Session, current_user):
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(TransformedImage.id == transformed_id and Image.user_id == current_user.id).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
    db.delete(transformed_image)
    db.commit()
    return transformed_image


async def get_qrcode_transformed_image_by_id(transformed_id: int, db: Session, current_user):
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(TransformedImage.id == transformed_id and Image.user_id == current_user.id).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
    url_to_qrcode = transformed_image.transform_image_url
    create_qrcode(url_to_qrcode)
    return transformed_image


async def get_url_transformed_image_by_id(transformed_id: int, db: Session, current_user):
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(TransformedImage.id == transformed_id and Image.user_id == current_user.id).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
    return transformed_image


async def get_transformed_img_by_user_id(user_id: int, db: Session, current_user):
    transformed_images = db.query(TransformedImage).join(Image). \
        filter(Image.user_id == user_id and Image.user_id == current_user.id).all()
    if not transformed_images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
    return transformed_images
