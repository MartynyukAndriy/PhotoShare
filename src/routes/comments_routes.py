from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi_limiter import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.comment_schemas import CommentResponse, CommentModel
from src.repository import comments as repository_comments

router = APIRouter(prefix='/comments', tags=['comments'])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator, Role.user])
access_delete = RolesAccess([Role.admin, Role.moderator])


@router.get('/', response_model=List[CommentResponse],
            dependencies=[Depends(RateLimiter(times=5, seconds=2)), Depends(access_get)])
async def get_comments(db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    comments = await repository_comments.get_comments(db)
    return comments


@router.get('/{comment_id}', response_model=CommentResponse, dependencies=[Depends(access_get)])
async def get_comment_by_id(comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                            _: User = Depends(auth_service.get_current_user)):
    comment = await repository_comments.get_comment_by_id(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment")
    return comment


@router.post('/', response_model=CommentResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=2, seconds=5)), Depends(access_create)])
async def create_comment(body: CommentModel, db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    comment = await repository_comments.create_comment(body, db)
    return comment


@router.put('/{comment_id}', response_model=CommentResponse, dependencies=[Depends(access_update)])
async def update_comment(body: CommentModel, comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    comment = await repository_comments.update_comment(body, comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment")
    return comment


@router.delete('/{comment_id}', response_model=CommentResponse, dependencies=[Depends(access_delete)])
async def remove_comment(comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    comment = await repository_comments.remove_comment(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment")
    return comment