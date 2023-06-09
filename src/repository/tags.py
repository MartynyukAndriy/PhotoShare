from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

#from src.database.models import Tag, User
from src.database.tag_models import Tag, User
# from src.schemas import TagModel
from src.schemas.tag_schemas import TagModel


async def get_tags(skip: int, limit: int, db: Session) -> List[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, db: Session) -> Tag:
    return db.query(Tag).filter(Tag.id == tag_id).first()


async def create_tag(body: TagModel, user: User, db: Session) -> Tag:
    tag = Tag(name=body.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagModel, user: User, db: Session) -> Tag | None:
    if user.role in ["administrator", "moderator"]:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            tag.name = body.name
            db.commit()
        return tag
    else:
        return None


async def remove_tag(tag_id: int, user: User, db: Session)  -> Tag | None:
    if user.role in ["administrator", "moderator"]:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            db.delete(tag)
            db.commit()
        return tag
    else:
        return None

