from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class TransformedImage(Base):
    __tablename__ = 'transformed_images'
    id = Column(Integer, primary_key=True)
    transform_image_url = Column(String(), nullable=False)
    image_id = Column(Integer, ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref='transformed_images')
