from fastapi import Depends, HTTPException, status
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from src.database.models import Image, User, Tag, Rating
from src.database.db import get_db


def find_image_by_tag(skip: int, limit: int, search: str | None, filter_type: int, db: Session, user: User):
    if search:
        search = search.lower().strip()
    else:
        search = ''
    if filter_type == 1:
        images = db.query(Image.url, Image.description) \
            .select_from(Image).join(Tag) \
            .filter(Tag.name == search) \
            .order_by(desc(Image.created_at)) \
            .offset(skip) \
            .limit(limit) \
            .all()
    elif filter_type == -1:
        images = db.query(Image.url, Image.description) \
            .select_from(Image).join(Tag) \
            .filter(Tag.name == search) \
            .order_by(asc(Image.created_at)) \
            .offset(skip) \
            .limit(limit) \
            .all()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="parameter filter_type must be '1" or '-1')

    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images not found for this tag")
    return images
