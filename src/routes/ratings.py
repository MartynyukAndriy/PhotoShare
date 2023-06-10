from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.rating_schemas import RatingModel, RatingResponse
from src.repository import ratings as repository_ratings
from src.conf.messages import AuthMessages

from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/ratings', tags=["ratings"])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator, Role.user])
access_delete = RolesAccess([Role.admin, Role.moderator])

@router.get("/image/{image_id}", response_model=int, dependencies=[Depends(access_get)])
async def get_common_rating(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    tags = await repository_ratings.get_average_rating(image_id, db)
    return tags


@router.get("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(access_get)])
async def read_tag(rating_id: int, db: Session = Depends(get_db)):
    rating = await repository_ratings.get_rating(rating_id, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    return rating


@router.post("/{image_id}", response_model=RatingResponse, dependencies=[Depends(access_create)])
async def create_rating(image_id, body: RatingModel, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    rating = await repository_ratings.create_rating_from_user(image_id, body, current_user, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't rate your images or rate more than 2 times")


@router.put("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(access_update)])
async def update_rating(body: RatingModel, rating_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    rating = await repository_ratings.update_rating(rating_id, body, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found or you don't have enough rules to update")
    return rating


@router.delete("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(access_delete)])
async def remove_rating(rating_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    rating = await repository_ratings.remove_rating(rating_id, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found or you don't have enough rules to delete")
    return rating
