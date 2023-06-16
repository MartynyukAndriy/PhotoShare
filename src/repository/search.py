from fastapi import Depends, HTTPException, status
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session
from typing import Optional
from src.database.models import Image, User, Tag, Rating, image_m2m_tag, Role
from src.database.db import get_db


async def get_img_by_user_id(user_id: int, db: Session, user):
    if user.role in (Role.admin, Role.moderator):
        images = db.query(Image).filter(Image.user_id == user_id).order_by(Image.id).all()
        if not images:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images for this user not found")
        return images
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin and moderator can get this data")


def find_image_by_tag(skip: int, limit: int, search: str, filter_type: str, db: Session, user: User):
    search = search.lower().strip()
    images = []
    if filter_type == "d":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag).filter(Tag.name==search)\
            .order_by(desc(Image.created_at)) \
            .offset(skip).limit(limit).all()
    elif filter_type == "-d":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag).filter(Tag.name==search)\
            .order_by(asc(Image.created_at)) \
            .offset(skip).limit(limit).all()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="parameter filter_type must be 'd" or '-d')
    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images not found for this tag")
    return images
