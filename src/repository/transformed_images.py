import cloudinary
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import TransformedImage, Image, User, Role
from src.database.db import get_db
from src.schemas.transformed_image_schemas import TransformedImageModel
from src.services.transformed_image import create_qrcode, create_transformations


async def create_transformed_picture(body: TransformedImageModel,
                                     current_user,
                                     image_id: int,
                                     db: Session = Depends(get_db)):
    """
    The create_transformed_picture function takes in a TransformedImageModel object, the current user, and an image id.
    It then queries the database for an Image with that id and checks if it belongs to the current user. If not, it raises
    a 404 error. Otherwise, it creates transformations from the body of data passed in by calling create_transformations().
    It then uses Cloudinary's build_url() function to generate a new url for this transformed image using those transformations.
    Finally, we add this new TransformedImage object to our database and return its information.

    :param body: TransformedImageModel: Get the transformation parameters from the request body
    :param current_user: Get the user that is currently logged in
    :param image_id: int: Get the original image from the database
    :param db: Session: Get the database session
    :return: A TransformedImageModel object
    """
    original_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()
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
    """
    The get_all_transformed_images function returns a list of all transformed images for the given image.
        The function takes in an integer skip, limit, and image_id as parameters. It also takes in a database session
        and current user object from the request context.

    :param skip: int: Skip a number of images in the database
    :param limit: int: Limit the number of transformed images that are returned
    :param image_id: int: Filter the transformed images by image_id
    :param db: Session: Pass the database session to the function
    :param current_user: Get the user id of the current logged in user
    :return: A list of all transformed images for a given image
    """
    transformed_list = db.query(TransformedImage).join(Image). \
        filter(and_(TransformedImage.image_id == image_id, Image.user_id == current_user.id)). \
        offset(skip).limit(limit).all()
    if not transformed_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed images for this image not found or user is not owner of this image")
    return transformed_list


async def get_transformed_img_by_id(transformed_id: int, db: Session, current_user):
    """
    The get_transformed_img_by_id function takes in a transformed_id and db Session object,
    and returns the TransformedImage with that id. If no such image exists, it raises an HTTPException.

    :param transformed_id: int: Get the transformed image by id
    :param db: Session: Pass the database session to the function
    :param current_user: Check if the user is authorized to access this image
    :return: A transformed image by its id
    """
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(and_(TransformedImage.id == transformed_id, Image.user_id == current_user.id)).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found or user is not owner of this image")
    return transformed_image


async def delete_transformed_image_by_id(transformed_id: int, db: Session, user):
    """
    The delete_transformed_image_by_id function deletes a transformed image from the database.
        It takes in an integer representing the id of the transformed image to be deleted, and a Session object for
        interacting with our database. The function returns a TransformedImage object representing the deleted
        transformed image.

    :param transformed_id: int: Identify the transformed image to be deleted
    :param db: Session: Access the database
    :param user: Check if the user is authorized to delete the image
    :return: The deleted transformed image
    """
    if user.role == Role.admin:
        transformed_image = db.query(TransformedImage).join(Image). \
            filter(TransformedImage.id == transformed_id).first()
        if not transformed_image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
        db.delete(transformed_image)
        db.commit()
        return transformed_image
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the admin can delete this data")


async def get_qrcode_transformed_image_by_id(transformed_id: int, db: Session, current_user):
    """
    The get_qrcode_transformed_image_by_id function takes in a transformed_id and db,
    and returns the transformed image with that id. If no such image exists, it raises an HTTPException.

    :param transformed_id: int: Get the transformed image by id
    :param db: Session: Pass the database session to the function
    :param current_user: Check if the user is logged in
    :return: The transformed image by id
    """
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(and_(TransformedImage.id == transformed_id, Image.user_id == current_user.id)).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found or user is not owner of this image")
    url_to_qrcode = transformed_image.transform_image_url
    create_qrcode(url_to_qrcode)
    return transformed_image


async def get_url_transformed_image_by_id(transformed_id: int, db: Session, current_user):
    """
    The get_url_transformed_image_by_id function takes in a transformed_id and db,
    and returns the url of the transformed image with that id.


    :param transformed_id: int: Get the transformed image by id
    :param db: Session: Access the database
    :param current_user: Check if the user is authorized to access the image
    :return: The transformed image url
    """
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(and_(TransformedImage.id == transformed_id, Image.user_id == current_user.id)).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found or user is not owner of this image")
    return transformed_image

