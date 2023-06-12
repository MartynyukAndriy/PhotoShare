from sqlalchemy.orm import Session

from src.database.models import Image, User
from src.schemas.image_schemas import ImageUpdateModel


async def add_image(db: Session, description: str, url: str, public_name: str, user: User):
    if not user:
        return None
    # Save picture in the database
    db_image = Image(description=description, url=url, public_name=public_name, user_id=user.id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


async def get_images(db: Session, user: User):
    return db.query(Image).filter(Image.user_id == user.id).all()


async def get_image(db: Session, id: int, user: User):
    return db.query(Image).filter(Image.id == id and Image.user_id == user.id).first()


async def update_image(db: Session, image: ImageUpdateModel, user: User):
    db_image = db.query(Image).filter(Image.id == image.id and Image.user_id == user.id).first()
    db_image.description = image.description
    db.commit()
    db.refresh(db_image)
    return db_image


async def delete_image(db: Session, id: int, user: User):
    db_image = db.query(Image).filter(Image.id == id and Image.user_id == user.id).first()
    db.delete(db_image)
    db.commit()
    return db_image
