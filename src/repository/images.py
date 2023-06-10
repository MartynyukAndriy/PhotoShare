from sqlalchemy.orm import Session

from src.database import models
from src.schemas import schemas


async def add_image(db: Session, description: str, url: str):
    # Save picture in the database
    db_image = models.Image(description=description, url=url)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


async def get_image(db: Session, id: int):
    return db.query(models.Image).filter(models.Image.id == id).first()


async def update_image(db: Session, image: schemas.ImageUpdateModel):
    db_image = db.query(models.Image).filter(models.Image.id == image.id).first()
    db_image.description = image.description
    db.commit()
    db.refresh(db_image)
    return db_image


async def delete_image(db: Session, id: int):
    db_image = db.query(models.Image).filter(models.Image.id == id).first()
    db.delete(db_image)
    db.commit()
    return db_image
