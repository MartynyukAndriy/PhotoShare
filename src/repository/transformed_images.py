import cloudinary
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import TransformedImage, Image
from src.database.db import get_db
from src.schemas.transformed_image_schemas import TransformedImageModel
from src.services.transformed_image import create_qrcode


async def create_transformed_picture(body: TransformedImageModel, image_id: int, db: Session = Depends(get_db)):
    original_image = db.query(Image).filter(Image.id == image_id).first()
    print(original_image)
    if not original_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Original image not found")

    transformations = []
    if body.width:
        width = {'width': body.width}
        transformations.append(width)
    if body.height:
        height = {'height': body.height}
        transformations.append(height)
    if body.crop:
        crop = {'crop': body.crop}
        transformations.append(crop)
    if body.angle:
        angle = {'angle': body.angle}
        transformations.append(angle)
    # if body.effect:
    #     effect = {'effect': body.effect}
    #     transformations.append(effect)

    print(transformations)

    public_id = original_image.public_name
    print(public_id)
    new_url = cloudinary.CloudinaryImage(public_id).build_url(transformation=transformations)

    # check is there such transformed image in the database already
    transformed_list = db.query(TransformedImage).filter(TransformedImage.image_id == image_id).all()
    if any([image.transform_image_url == new_url for image in transformed_list]):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This transformed images is already exists")

    new_transformed_image = TransformedImage(transform_image_url=new_url, image_id=original_image.id)
    db.add(new_transformed_image)
    db.commit()
    db.refresh(new_transformed_image)
    return new_transformed_image


async def get_all_transformed_images(skip: int, limit: int, image_id: int, db: Session):
    transformed_list = db.query(TransformedImage).filter(TransformedImage.image_id == image_id).offset(skip).limit(
        limit).all()
    if not transformed_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed images for this image not found")
    return transformed_list


async def get_transformed_image_by_id(transformed_id: int, db: Session):
    transformed_image = db.query(TransformedImage).filter(TransformedImage.id == transformed_id).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
    return transformed_image


async def delete_transformed_image_by_id(transformed_id: int, db: Session):
    transformed_image = db.query(TransformedImage).filter(TransformedImage.id == transformed_id).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
    db.delete(transformed_image)
    db.commit()
    return transformed_image


async def get_qrcode_transformed_image_by_id(transformed_id: int, db: Session):
    transformed_image = db.query(TransformedImage).filter(TransformedImage.id == transformed_id).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
    url_to_qrcode = transformed_image.transform_image_url
    return create_qrcode(url_to_qrcode)
