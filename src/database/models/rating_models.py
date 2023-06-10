from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, PickleType
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Rating(Base):

    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(PickleType)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="comments")
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="comments")
