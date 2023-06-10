from sqlalchemy import Column, Integer, String, Table, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from src.database.roles import Role

Base = declarative_base()

# змінити назву image/images на актуальну
image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


#видалити цей клас
class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    tags = relationship("Tag", secondary=image_m2m_tag, backref="images")

"""
в клас Image(Base) додати
tags = relationship("Tag", secondary=image_m2m_tag, backref="images")
"""

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)

