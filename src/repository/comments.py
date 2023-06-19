from sqlalchemy.orm import Session

from src.database.models import Comment, Image
from src.schemas.comment_schemas import CommentModel


async def get_comments(db: Session):
    """
    The get_comments function returns all comments in the database.
    
    :param db: Session: Pass the database session to the function
    :return: All the comments from the database
    """
    return db.query(Comment).all()


async def get_comment_by_id(comment_id: int, db: Session):
    """
    The get_comment_by_id function returns a comment object from the database based on its id.
        
    
    :param comment_id: int: Filter the database for a specific comment
    :param db: Session: Pass the database session to the function
    :return: A comment object
    """
    return db.query(Comment).filter_by(id=comment_id).first()


async def create_comment(body: CommentModel, db: Session):
    """
    The create_comment function creates a new comment in the database.
        
    
    :param body: CommentModel: Pass the data to be used in creating a new comment
    :param db: Session: Pass the database session to the function
    :return: A comment object
    """
    comment = Comment(**body.dict())
    db.add(comment)
    db.commit()
    return comment


async def update_comment(body: CommentModel, comment_id, db: Session):
    """
    The update_comment function updates a comment in the database.
        Args:
            body (CommentModel): The CommentModel object to update.
            comment_id (int): The id of the CommentModel object to update.
            db (Session, optional): SQLAlchemy Session instance. Defaults to None.
        Returns:
            Optional[Comment]: A dictionary containing information about the updated Comment or None if no such comment exists.
    
    :param body: CommentModel: Pass the updated comment into the function
    :param comment_id: Get the comment from the database
    :param db: Session: Pass the database session to the function
    :return: The comment object
    """
    comment = await get_comment_by_id(comment_id, db)
    if comment:
        comment.comment = body.comment
        db.commit()
    return comment


async def remove_comment(comment_id, db: Session):
    """
    The remove_comment function removes a comment from the database.
        Args:
            comment_id (int): The id of the comment to be removed.
            db (Session): A connection to the database.
        Returns:
            Comment: The deleted Comment object.
    
    :param comment_id: Find the comment to be deleted
    :param db: Session: Pass the database session to the function
    :return: The comment that was deleted
    """
    comment = await get_comment_by_id(comment_id, db)
    if comment:
        db.delete(comment)
        db.commit()
    return comment


async def get_image_by_id(image_id: int, db: Session):
    """
    The get_image_by_id function takes in an image_id and a database session,
    and returns the Image object with that id. If no such image exists, it returns None.

    :param image_id: int: Specify the id of the image to be retrieved
    :param db: Session: Pass the database session to the function
    :return: The image with the given id
    """
    image = db.query(Image).filter_by(id=image_id).first()
    return image
