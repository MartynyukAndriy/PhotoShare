from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
from src.database.roles import Role

Base = declarative_base()


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


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)

    # TODO add roles
    role = Column("role", Enum(Role), default=Role.user)
