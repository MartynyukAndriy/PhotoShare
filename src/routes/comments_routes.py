from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role, Image
from src.schemas.comment_schemas import CommentResponse, CommentModel, CommentDeleteResponse
from src.repository import comments as repository_comments
from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/comments', tags=['comments'])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator, Role.user])
access_delete = RolesAccess([Role.admin, Role.moderator])


@router.get('/', response_model=List[CommentResponse],
            dependencies=[Depends(RateLimiter(times=5, seconds=2)), Depends(access_get)])
async def get_comments(db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
    The get_comments function returns a list of comments from the database.
        
    
    :param db: Session: Pass the database session to the function
    :param _: User: Check if the user is authenticated
    :return: A list of comments
    """
    comments = await repository_comments.get_comments(db)
    return comments


@router.get('/{comment_id}', response_model=CommentResponse, dependencies=[Depends(access_get)])
async def get_comment_by_id(comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                            _: User = Depends(auth_service.get_current_user)):
    """
    The get_comment_by_id function returns a comment by its id.
        Args:
            comment_id (int): The id of the comment to be returned.
            db (Session, optional): A database session object for querying the database. Defaults to Depends(get_db).
            _ (User, optional): An authenticated user object for checking if the user is authorized to access this endpoint. Defaults to Depends(auth_service.get_current_user).
    
    :param comment_id: int: Get the comment id from the url
    :param db: Session: Pass the database session to the repository layer
    :param _: User: Get the current user
    :return: A comment object
    """
    comment = await repository_comments.get_comment_by_id(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment")
    return comment


@router.post('/', response_model=CommentResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=2, seconds=5)), Depends(access_create)])
async def create_comment(body: CommentModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_comment function creates a new comment in the database.
        The function takes a CommentModel object as input, and returns the newly created comment.
    
    :param body: CommentModel: Create a comment object from the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user_id of the current user
    :return: The comment object
    """
    try:
        image = db.query(Image).filter_by(id=image_id).first()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such image")
    body.user_id = current_user.id
    comment = await repository_comments.create_comment(body, db)
    return comment


@router.put('/{comment_id}', response_model=CommentResponse, dependencies=[Depends(access_update)])
async def update_comment(body: CommentModel, comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_comment function updates a comment in the database.
        
    
    :param body: CommentModel: Get the comment body from the request
    :param comment_id: int: Get the comment id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the user who is currently logged in
    :return: The updated comment
    """
    if current_user.id != body.user_id and current_user.role == 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't change not your comment")
    comment = await repository_comments.update_comment(body, comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment")
    return comment


@router.delete('/{comment_id}', response_model=CommentDeleteResponse, dependencies=[Depends(access_delete)])
async def remove_comment(comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    """
    The remove_comment function removes a comment from the database.
        Args:
            comment_id (int): The id of the comment to be removed.
            db (Session, optional): A database session object used for querying and modifying data in the database. Defaults to Depends(get_db).
            _ (User, optional): An object representing an authenticated user making this request. Defaults to Depends(auth_service.get_current_user).
    
    :param comment_id: int: Get the comment id from the path
    :param db: Session: Pass the database connection to the function
    :param _: User: Get the current user from the auth_service
    :return: A comment object
    """
    comment = await repository_comments.remove_comment(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment")
    return comment
