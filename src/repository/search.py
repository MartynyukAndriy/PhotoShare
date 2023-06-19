from fastapi import Depends, HTTPException, status
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session
from src.database.models import Image, User, Tag, Rating, image_m2m_tag, Role
from src.database.db import get_db


def calc_average_rating(image_id, db: Session):
    """
    The calc_average_rating function calculates the average rating for a given image.
        Args:
            image_id (int): The id of the image to calculate an average rating for.

    :param image_id: Identify the image in the database
    :param db: Session: Pass in the database session, so that we can use it to query the database
    :return: The average rating of an image
    """

    image_ratings = db.query(Rating).filter(Rating.image_id == image_id).all()
    if len(image_ratings) == 0:
        return 0
    sum_user_rating = 0
    for element in image_ratings:
        if element.one_star:
            sum_user_rating += 1
        if element.two_stars:
            sum_user_rating += 2
        if element.three_stars:
            sum_user_rating += 3
        if element.four_stars:
            sum_user_rating += 4
        if element.five_stars:
            sum_user_rating += 5
    average_user_rating = sum_user_rating / len(image_ratings)
    return average_user_rating


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
            images = db.query(Image).filter(Image.user_id == user_id).order_by(desc(Image.created_at)).offset(
                skip).limit(limit).all()
        elif filter_type == "-d":
            images = db.query(Image).filter(Image.user_id == user_id).order_by(asc(Image.created_at)).offset(
                skip).limit(limit).all()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="parameter filter_type must be 'd" or '-d')
        if not images:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images for this user not found")
        return images
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin or moderator can get this data")


async def find_image_by_tag(skip: int, limit: int, search: str, filter_type: str, db: Session, user: User):
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
            .join(Tag).filter(Tag.name == search) \
            .order_by(desc(Image.created_at)) \
            .offset(skip).limit(limit).all()
    elif filter_type == "-d":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag).filter(Tag.name == search) \
            .order_by(asc(Image.created_at)) \
            .offset(skip).limit(limit).all()
    elif filter_type == "r":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag).join(Rating).filter(Tag.name == search) \
            .offset(skip).limit(limit).all()

        images_rating_list = list(map(lambda x: (x.id, calc_average_rating(x.id, db)), images))
        sorted_images_rating_list = sorted(images_rating_list, key=lambda x: x[1], reverse=False)
        final_images = []
        for img_rating in sorted_images_rating_list:
            for image in images:
                if img_rating[0] == image.id:
                    image.rating = img_rating[1]
                    final_images.append(image)
        images = final_images
    elif filter_type == "-r":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag).join(Rating).filter(Tag.name == search) \
            .offset(skip).limit(limit).all()
        images_rating_list = list(map(lambda x: (x.id, calc_average_rating(x.id, db)), images))
        sorted_images_rating_list = sorted(images_rating_list, key=lambda x: x[1], reverse=True)
        print(images_rating_list)
        print(sorted_images_rating_list)
        final_images = []
        for img_rating in sorted_images_rating_list:
            for image in images:
                if img_rating[0] == image.id:
                    image.rating = img_rating[1]
                    final_images.append(image)
        images = final_images
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="parameter filter_type must be 'd' / '-d' for sorting by date or 'r' / '-r' for sorting by rating)")
    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images not found for this tag")
    return images
