import enum

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean, Enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import Table

Base = declarative_base()


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String(255))
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="comments")
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="comments")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)


class TransformedImage(Base):
    __tablename__ = 'transformed_images'
    id = Column(Integer, primary_key=True)
    transform_image_url = Column(String(), nullable=False)
    qrcode_image_url = Column(String(), nullable=False)
    image_id = Column(Integer, ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref='transformed_images')
    created_at = Column(DateTime, default=func.now())


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    photo_count = Column(Integer, default=0)
    refresh_token = Column(String(255), nullable=True)
    role = Column('role', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    one_star = Column(Boolean, default=False)
    two_stars = Column(Boolean, default=False)
    three_stars = Column(Boolean, default=False)
    four_stars = Column(Boolean, default=False)
    five_stars = Column(Boolean, default=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="ratings")
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="ratings")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(300), unique=True, index=True)
    description = Column(String(500), nullable=True)
    public_name = Column(String(), unique=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="images")
    tags = relationship("Tag", secondary=image_m2m_tag, backref="images")
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
