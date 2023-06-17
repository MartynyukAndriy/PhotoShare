from fastapi import Depends, HTTPException, status
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session
from typing import Optional
from src.database.models import Image, User, Tag, Rating, image_m2m_tag, Role
from src.database.db import get_db


async def get_img_by_user_id(user_id, skip, limit, filter_type, db, user):
    """
    The get_img_by_user_id function is used to get all images for a specific user.
        It takes in the following parameters:
            - user_id: The id of the user whose images are being requested.
            - skip: The number of records to skip before returning results (for pagination).  Default value is 0.
            - limit: The maximum number of records to return (for pagination).  Default value is 10.

    :param user_id: Filter the images by user_id
    :param skip: Skip the first n images
    :param limit: Limit the number of images returned
    :param filter_type: Determine whether the images should be returned in ascending or descending order
    :param db: Make a query to the database
    :param user: Check if the user is an admin or moderator
    :return: A list of images for a specific user
    """
    if user.role in (Role.admin, Role.moderator):
        if filter_type == "d":
            images = db.query(Image).filter(Image.user_id == user_id).order_by(desc(Image.created_at)).offset(skip).limit(limit).all()
        elif filter_type == "-d":
            images = db.query(Image).filter(Image.user_id == user_id).order_by(asc(Image.created_at)).offset(skip).limit(limit).all()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="parameter filter_type must be 'd" or '-d')
        if not images:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images for this user not found")
        return images
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin or moderator can get this data")


def find_image_by_tag(skip: int, limit: int, search: str, filter_type: str, db: Session, user: User):
    """
    The find_image_by_tag function takes in a skip, limit, search string and filter_type.
    It then queries the database for images that match the search string and returns them to the user.


    :param skip: int: Skip a number of images
    :param limit: int: Limit the number of images returned
    :param search: str: Search for the tag name
    :param filter_type: str: Determine whether the images are sorted by date in ascending or descending order
    :param db: Session: Access the database
    :param user: User: Get the user_id of the current logged in user
    :return: A list of images
    """
    search = search.lower().strip()
    images = []
    if filter_type == "d":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag).filter(Tag.name==search)\
            .order_by(desc(Image.created_at)) \
            .offset(skip).limit(limit).all()
    elif filter_type == "-d":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag).filter(Tag.name==search)\
            .order_by(asc(Image.created_at)) \
            .offset(skip).limit(limit).all()
        print(images)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="parameter filter_type must be 'd" or '-d')
    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images not found for this tag")
    return images
