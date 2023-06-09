from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.database.db import Base, engine


class Picture(Base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)


class TransformedPicture(Base):
    __tablename__ = 'transformed_pictures'
    id = Column(Integer, primary_key=True)
    true_img_id = Column(Integer, ForeignKey('pictures.id', ondelete='CASCADE'), default=None)
    transform_img_url = Column(String(), nullable=False)
    picture = relationship('Picture', backref='transformed_pictures')


Base.metadata.create_all(bind=engine)
