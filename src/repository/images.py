from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Image, User, Tag, Comment, Role
from src.repository.ratings import get_average_rating
from src.schemas.image_schemas import ImageUpdateModel, ImageAddModel, ImageAddTagModel
from src.services.images import images_service_normalize_tags


async def get_images(db: Session, user: User):
    """
    The get_images function returns a list of images and their associated ratings and comments.
        If the user is an admin, all images are returned. Otherwise, only the user's own images are returned.

    :param db: Session: Pass in a database session to the function
    :param user: User: Determine if the user is an admin or a regular user
    :return: A list of dictionaries, each dictionary containing an image object and its associated ratings
    """

    # if user.role == Role.admin:
    # images = db.query(Image).order_by(Image.id).all()
    # else:
    images = db.query(Image).order_by(Image.id).all()

    user_response = []
    for image in images:
        ratings = await get_average_rating(image.id, db)
        comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == user.id).all()
        user_response.append({"image": image, "ratings": ratings, "comments": comments})
    return user_response


async def get_image(db: Session, id: int, user: User):
    """
    The get_image function takes in a database session, an image id, and a user.
    If the user is an admin, it returns the image with that id from the database.
    Otherwise it returns only images with that id which belong to that user.

    :param db: Session: Get access to the database
    :param id: int: Specify the id of the image that is being requested
    :param user: User: Check if the user is an admin or not
    :return: A tuple of the image, ratings and comments
    """

    # if user.role == Role.admin:
    #     image = db.query(Image).filter(Image.id == id).first()
    # else:
    image = db.query(Image).filter(Image.id == id).first()

    if image:
        ratings = await get_average_rating(image.id, db)
        comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == user.id).all()
        return image, ratings, comments
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def admin_get_image(db: Session, user_id: id):
    """
    The admin_get_image function is used to get all images for a specific user.
        The function takes in the database session and the user_id of the desired user.
        It then queries for all images with that specific id, orders them by their id, and returns them as an array of objects.


    :param db: Session: Connect to the database
    :param user_id: id: Get the images of a specific user
    :return: All the images in the database for a specific user
    """

    images = db.query(Image).filter(Image.user_id == user_id).order_by(Image.id).all()
    if images:
        user_response = []
        for image in images:
            ratings = await get_average_rating(image.id, db)
            comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == image.user_id).all()
            user_response.append({"image": image, "ratings": ratings, "comments": comments})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return user_response


async def add_image(db: Session, image: ImageAddModel, tags: list[str], url: str, public_name: str, user: User):

    """
    The add_image function adds an image to the database.
        Args:
            db (Session): The database session object.
            image (ImageAddModel): The ImageAddModel object containing the information about the new image.
            tags (list[str]): A list of strings representing tags for this new image.  Each tag is a string with a maximum length of 25 characters, and there can be up to 5 tags per picture in our system.  If more than 5 are provided, only the first five will be used and saved in our system; any additional ones will be ignored by this function call but not discarded from

    :param db: Session: Access the database
    :param image: ImageAddModel: Get the description of the image
    :param tags: list[str]: Add tags to the image
    :param url: str: Store the url of the image
    :param public_name: str: Save the name of the image in the database
    :param user: User: Get the user id from the database
    :return: A tuple of two elements: the image and a string
    """
    if not user:
        return None

    detail = ""
    num_tags = 0
    image_tags = []
    for tag in tags:
        if len(tag) > 25:
            tag = tag[0:25]
        if not db.query(Tag).filter(Tag.name == tag.lower()).first():
            db_tag = Tag(name=tag.lower())
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
        if num_tags < 5:
            image_tags.append(tag.lower())
        num_tags += 1

    if num_tags >= 5:
        detail = " But be attentive you can add only five tags to an image"

    tags = db.query(Tag).filter(Tag.name.in_(image_tags)).all()
    # Save picture in the database
    db_image = Image(description=image.description, tags=tags, url=url, public_name=public_name, user_id=user.id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image, detail


async def update_image(db: Session, image_id, image: ImageUpdateModel, user: User):
    """
    The update_image function updates an image description in the database.
        Args:
            db (Session): The SQLAlchemy session object.
            image_id (int): The id of the image to update.
            image (ImageUpdateModel): An ImageUpdateModel object containing the new values for updating an existing Image record in the database.

    :param db: Session: Access the database
    :param image_id: Find the image in the database
    :param image: ImageUpdateModel: Pass the image update model
    :param user: User: Check if the user is an admin or not
    :return: A db_image
    """

    if user.role == Role.admin:
        db_image = db.query(Image).filter(Image.id == image_id).first()
    else:
        db_image = db.query(Image).filter(Image.id == image_id, Image.user_id == user.id).first()

    if db_image:
        db_image.description = image.description
        db.commit()
        db.refresh(db_image)
        return db_image
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def add_tag(db: Session, image_id, body: ImageAddTagModel, user: User):
    """
    The add_tag function adds tags to an image.

    :param db: Session: Access the database
    :param image_id: Identify the image to which the tags are added
    :param body: ImageAddTagModel: Get the tags from the request body
    :param user: User: Check if the user is an admin or not
    :return: The image object with the updated tags
    """
    tags = await images_service_normalize_tags(body)

    detail = ""
    num_tags = 0
    image_tags = []
    for tag in tags:
        if tag:
            if len(tag) > 25:
                tag = tag[0:25]
            if not db.query(Tag).filter(Tag.name == tag.lower()).first():
                db_tag = Tag(name=tag.lower())
                db.add(db_tag)
                db.commit()
                db.refresh(db_tag)
            if num_tags < 5:
                image_tags.append(tag.lower())
            num_tags += 1

    if num_tags >= 5:
        detail = "But be attentive you can add only five tags to an image"

    tags = db.query(Tag).filter(Tag.name.in_(image_tags)).all()

    if user.role == Role.admin:
        image = db.query(Image).filter(Image.id == image_id).first()
    else:
        image = db.query(Image).filter(Image.id == image_id, Image.user_id == user.id).first()

    if image:
        image.updated_at = datetime.utcnow()
        image.tags = tags
        db.commit()
        db.refresh(image)
        return image, detail
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def delete_image(db: Session, id: int, user: User):
    """
    The delete_image function deletes an image from the database.
        Args:
            db (Session): The database session object.
            id (int): The ID of the image to delete.
            user (User): The user who is deleting the image.

    :param db: Session: Access the database
    :param id: int: Specify the id of the image to be deleted
    :param user: User: Check if the user is an admin or not
    :return: The deleted image
    """

    if user.role == Role.admin:
        db_image = db.query(Image).filter(Image.id == id).first()
    else:
        db_image = db.query(Image).filter(Image.id == id, Image.user_id == user.id).first()

    if db_image:
        db.delete(db_image)
        db.commit()
        return db_image
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
