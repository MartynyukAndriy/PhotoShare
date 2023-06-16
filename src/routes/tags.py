from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.tag_schemas import TagModel, TagResponse
from src.repository import tags as repository_tags
from src.conf.messages import AuthMessages

from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/tags', tags=["tags"])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator])
access_delete = RolesAccess([Role.admin, Role.moderator])


@router.get("/", response_model=List[TagResponse], dependencies=[Depends(access_get)])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
    The read_tags function returns a list of tags.
    
    :param skip: int: Skip the first n tags
    :param limit: int: Limit the number of tags returned
    :param db: Session: Pass the database session to the function
    :param _: User: Tell fastapi that the user is required, but it will not be used in the function
    :return: A list of tags
    """
    tags = await repository_tags.get_tags(skip, limit, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse, dependencies=[Depends(access_get)])
async def read_tag(tag_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
    The read_tag function returns a single tag by its ID.
    
    :param tag_id: int: Specify the id of the tag to be deleted
    :param db: Session: Pass the database session to the function
    :param _: User: Check if the user is authenticated and has access to the endpoint
    :return: A tag object
    """
    tag = await repository_tags.get_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.post("/", response_model=TagResponse, dependencies=[Depends(access_create)])
async def create_tag(body: TagModel, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
    The create_tag function creates a new tag in the database.
        The function takes a TagModel object as input and returns the created tag.
        
    
    :param body: TagModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :param _: User: Get the current user
    :return: A tagmodel object
    """
    tag = await repository_tags.create_tag(body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=AuthMessages.verification_error)
    return tag


@router.put("/{tag_id}", response_model=TagResponse, dependencies=[Depends(access_update)])
async def update_tag(body: TagModel, tag_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
    The update_tag function updates a tag in the database.
        
    
    :param body: TagModel: Pass the data from the request body to the function
    :param tag_id: int: Identify the tag to be deleted
    :param db: Session: Pass the database session to the repository layer
    :param _: User: Get the current user from the auth_service
    :return: A tagmodel object
    """
    tag = await repository_tags.update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found or you don't have enough rules to update")
    return tag


@router.delete("/{tag_id}", response_model=TagResponse, dependencies=[Depends(access_delete)])
async def remove_tag(tag_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
    The remove_tag function removes a tag from the database.
        Args:
            tag_id (int): The id of the tag to be removed.
            db (Session, optional): A database session object for interacting with the database. Defaults to Depends(get_db).
            _ (User, optional): An authenticated user object for checking permissions and ownership of tags. Defaults to Depends(auth_service.get_current_user).
    
    :param tag_id: int: Specify the tag id of the tag to be deleted
    :param db: Session: Pass the database session to the function
    :param _: User: Get the current user
    :return: The removed tag
    """
    tag = await repository_tags.remove_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found or you don't have enough rules to delete")
    return tag
