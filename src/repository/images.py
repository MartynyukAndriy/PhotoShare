from sqlalchemy.orm import Session

from src.database.models import Image
from src.schemas.image_schemas import ImageUpdateModel


async def add_image(db: Session, description: str, url: str, public_name: str):
    # Save picture in the database
    db_image = Image(description=description, url=url, public_name=public_name)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


async def get_image(db: Session, id: int):
    return db.query(Image).filter(Image.id == id).first()


async def update_image(db: Session, image: ImageUpdateModel):
    db_image = db.query(Image).filter(Image.id == image.id).first()
    db_image.description = image.description
    db.commit()
    db.refresh(db_image)
    return db_image


async def delete_image(db: Session, id: int):
    db_image = db.query(Image).filter(Image.id == id).first()
    db.delete(db_image)
    db.commit()
    return db_image
