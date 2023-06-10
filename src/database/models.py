from sqlalchemy import Column, Integer, String, Boolean, func, Table, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# note_m2m_tag = Table(
#     "note_m2m_tag",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
#     Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
# )


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(300), unique=True, index=True)
    description = Column(String(500))
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    # user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    # user = relationship('User', backref='picture')
    #
    # tags = relationship("Tag", secondary=note_m2m_tag, backref="picture")
    # comments = relationship("Comment", secondary=note_m2m_tag, backref="picture")
