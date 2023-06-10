from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(300), unique=True, index=True)
    description = Column(String(500), nullable=True)
    public_name = Column(String(), unique=True)
    # user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    # user = relationship('User', backref="comments")
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())