from typing import List, Type

from sqlalchemy.orm import Session

from src.database.models import Tag
from src.schemas.tag_schemas import TagModel


async def get_tags(skip: int, limit: int, db: Session) -> List[Type[Tag]]:
    """
    The get_tags function returns a list of tags from the database.
    
    :param skip: int: Skip a number of records in the database
    :param limit: int: Limit the number of results returned
    :param db: Session: Access the database
    :return: A list of tag objects
    """
    return db.query(Tag).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, db: Session) -> Type[Tag] | None:
    """
    The get_tag function returns a Tag object from the database.
        
    
    :param tag_id: int: Filter the query to only return a tag with an id that matches the parameter
    :param db: Session: Pass the database session to the function
    :return: A tag object
    """
    return db.query(Tag).filter(Tag.id == tag_id).first()


async def create_tag(body: TagModel, db: Session) -> Tag:
    """
    The create_tag function creates a new tag in the database.
    
    The create_tag function takes a TagModel object as input and returns a Tag object.
    
    
    :param body: TagModel: Pass in the data that is being sent to the api
    :param db: Session: Pass the database session to the function
    :return: A tag
    """
    tag = Tag(name=body.name.lower())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    """
    The update_tag function updates a tag in the database.
        Args:
            tag_id (int): The id of the tag to update.
            body (TagModel): The updated TagModel object with new values for name and description.
            db (Session): A Session instance used to query the database.
        Returns:
            Tag | None: If successful, returns an updated Tag object; otherwise, returns None.
    
    :param tag_id: int: Identify the tag to be updated
    :param body: TagModel: Pass in the new tag name
    :param db: Session: Access the database
    :return: A tag object
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        new_tag_name_in_base = db.query(Tag).filter(Tag.name == body.name.lower()).first()
        if new_tag_name_in_base:
            return None
        tag.name = body.name.lower()
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session) -> Tag | None:
    """
    The remove_tag function removes a tag from the database.
        
    
    :param tag_id: int: Specify the id of the tag to be removed
    :param db: Session: Pass the database session to the function
    :return: A tag object
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session) -> Tag | None:
    """
    The remove_tag function removes a tag from the database.
        
    
    :param tag_id: int: Specify the id of the tag that is to be removed
    :param db: Session: Access the database
    :return: A tag object
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag


async def get_tag_by_name(tag_name: str, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.name == tag_name.lower()).first()
    return tag
