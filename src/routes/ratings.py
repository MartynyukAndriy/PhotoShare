from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.rating_schemas import RatingModel, RatingResponse, AverageRatingResponse
from src.repository import ratings as repository_ratings
from src.conf.messages import AuthMessages

from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/ratings', tags=["ratings"])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator])
access_delete = RolesAccess([Role.admin, Role.moderator])


@router.get("/image/{image_id}", response_model=float, dependencies=[Depends(access_get)])
async def common_image_rating(image_id, _: User = Depends(auth_service.get_current_user),
                              db: Session = Depends(get_db)):
    """
    The common_image_rating function returns the average rating of an image.
        Args:
            image_id (int): The id of the image to be rated.
            _ (User): The user who is making the request. This is a dependency injection, and it's used for authentication purposes only. It can be ignored when calling this function from outside FastAPI codebase, as it will automatically get injected by FastAPI itself when called from a route that requires authentication.
    
    :param image_id: Get the image from the database
    :param _: User: Get the current user from the auth_service
    :param db: Session: Pass the database session to the function
    :return: The average rating of an image
    """
    common_rating = await repository_ratings.get_average_rating(image_id, db)
    return common_rating


@router.get("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(access_get)])
async def read_rating(rating_id: int, _: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The read_rating function returns a rating by its ID.
        ---
        get:
          summary: Get a rating by ID.
          description: Returns the details of an individual rating, including the user who created it and their username.
          tags: [ratings]
          parameters:
            - in: path
              name: id_rating  # The unique identifier for this particular rating (e.g., 1) is passed as part of the URL path (e.g., /ratings/{id_rating}). This is called &quot;path binding&quot;. See https://fastapi
    
    :param rating_id: int: Identify the rating to be deleted
    :param _: User: Allow the auth_service to inject a user object into the function
    :param db: Session: Access the database
    :return: A rating object
    """
    rating = await repository_ratings.get_rating(rating_id, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    return rating


@router.post("/{image_id}", response_model=RatingResponse, dependencies=[Depends(access_create)])
async def create_rate(image_id, body: RatingModel, current_user: User = Depends(auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    """
    The create_tag function creates a new tag in the database.
        
    
    :param image_id: Get the image from the database
    :param body: RatingModel: Get the data from the request body
    :param current_user: User: Get the user who is currently logged in
    :param db: Session: Connect to the database
    :return: A tag object
    """
    rating = await repository_ratings.create_rating(image_id, body, current_user, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please, check the image_id. You can't rate your images or give 2 or more rates for 1 image")
    return rating


@router.put("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(access_update)])
async def update_rating(body: RatingModel, rating_id: int, db: Session = Depends(get_db),
                        _: User = Depends(auth_service.get_current_user)):
    """
    The update_rating function updates a rating in the database.
        
    
    :param body: RatingModel: Get the body of the request
    :param rating_id: int: Identify the rating to be updated
    :param db: Session: Pass the database connection to the function
    :param _: User: Get the current user from auth_service
    :return: A rating object
    """
    rating = await repository_ratings.update_rating(rating_id, body, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Rating not found or you can't update the rating because of rules or roles")
    return rating


@router.delete("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(access_delete)])
async def remove_rating(rating_id: int, db: Session = Depends(get_db),
                        _: User = Depends(auth_service.get_current_user)):
    """
    The remove_rating function removes a rating from the database.
        
    
    :param rating_id: int: Find the rating in the database
    :param db: Session: Get the database session
    :param _: User: Make sure that the user is logged in
    :return: The deleted rating
    """
    rating = await repository_ratings.remove_rating(rating_id, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Rating not found or you don't have enough rules to delete")
    return rating
