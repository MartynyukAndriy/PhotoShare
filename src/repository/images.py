from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Image, User, Tag, Comment, Role
from src.repository.ratings import get_average_rating
from src.schemas.image_schemas import ImageUpdateModel, ImageAddModel, ImageAddTagModel


async def get_images(db: Session, user: User):
    if user.role == Role.admin:
        images = db.query(Image).order_by(Image.id).all()
    else:
        images = db.query(Image).filter(Image.user_id == user.id).order_by(Image.id).all()

    user_response = []
    for image in images:
        ratings = await get_average_rating(image.id, db)
        comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == user.id).all()
        user_response.append({"image": image, "ratings": ratings, "comments": comments})
    return user_response


async def get_image(db: Session, id: int, user: User):
    if user.role == Role.admin:
        image = db.query(Image).filter(Image.id == id).first()
    else:
        image = db.query(Image).filter(Image.id == id, Image.user_id == user.id).first()

    if image:
        ratings = await get_average_rating(image.id, db)
        comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == user.id).all()
        return image, ratings, comments
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def admin_get_image(db: Session, user_id: id):
    images = db.query(Image).filter(Image.user_id == user_id).order_by(Image.id).all()
    print(images)
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
    if not user:
        return None

    for tag in tags:
        if len(tag) > 25:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Tag length should not exceed 25 characters'
            )
        if not db.query(Tag).filter(Tag.name == tag).first():
            tag = Tag(name=tag)
            db.add(tag)
            db.commit()
            db.refresh(tag)

    tags = db.query(Tag).filter(Tag.name.in_(tags)).all()
    # Save picture in the database
    db_image = Image(description=image.description, tags=tags, url=url, public_name=public_name, user_id=user.id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


async def update_image(db: Session, image_id, image: ImageUpdateModel, user: User):
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
    set_tags = set(body.tags)
    tags = set_tags
    if len(tags) > 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='No more than 5 tags are allowed'
        )

    for tag in tags:
        if len(tag) > 25:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Tag length should not exceed 25 characters'
            )
        if not db.query(Tag).filter(Tag.name == tag).first():
            tag = Tag(name=tag)
            db.add(tag)
            db.commit()
            db.refresh(tag)

    tags = db.query(Tag).filter(Tag.name.in_(tags)).all()

    if user.role == Role.admin:
        image = db.query(Image).filter(Image.id == image_id).first()
    else:
        image = db.query(Image).filter(Image.id == image_id, Image.user_id == user.id).first()

    if image:
        image.updated_at = datetime.utcnow()
        image.tags = tags
        db.commit()
        db.refresh(image)
        return image
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def delete_image(db: Session, id: int, user: User):
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
