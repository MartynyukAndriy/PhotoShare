from typing import List

from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository.search import find_image_by_tag
from src.routes.tags import access_get, access_delete, access_create
from src.schemas.image_schemas import ImageDb
from src.services.auth import auth_service
from src.repository.search import get_img_by_user_id

router = APIRouter(prefix="/search", tags=["search and filter"])


@router.get("/image/{user_id}", response_model=list[ImageDb],
            dependencies=[Depends(access_get)])
async def get_image_by_user_id(user_id: int = Path(ge=1),
                               db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_image_by_user_id function returns a list of images that are associated with the user_id.
        The function takes in an integer value for the user_id, and it also depends on a database session object
        and current_user object.  The function returns a list of image objects.

    :param user_id: int: Get the user_id from the path
    :param db: Session: Access the database
    :param current_user: User: Get the current user's id
    :return: A list of images for the user with the specified id
    """
    images = await get_img_by_user_id(user_id, db, current_user)
    return images


@router.get("/", response_model=List[ImageDb], dependencies=[Depends(access_get)])
async def search_images_by_tag(skip: int = 0, limit: int = 10,
                               search_tag: str = "",
                               filter_type: str = 'd',
                               db: Session = Depends(get_db),
                               user: User = Depends(auth_service.get_current_user)):
    """
    The search_images_by_tag function searches for images by tag.
        Args:
            skip (int): The number of images to skip in the search results. Default is 0.
            limit (int): The maximum number of images to return in the search results. Default is 10, max is 100.
            search_tag (str): A string containing a single tag or multiple tags separated by commas, e.g., &quot;dog&quot; or &quot;dog,cat&quot;.  If no tags are provided then all image records will be returned regardless of their associated tags.

    :param skip: int: Skip the first n images
    :param limit: int: Limit the number of images returned
    :param search_tag: str: Search for images by a tag
    :param filter_type: str: Determine whether the images are sorted by date 'd' or '-d' (reverse sort)
    :param db: Session: Get the database session
    :param user: User: Get the current user
    :return: A list of image objects
    """
    images = find_image_by_tag(skip, limit, search_tag, filter_type, db, user)
    return images
