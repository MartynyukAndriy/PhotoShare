from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_


from src.database.models import Rating, User
from src.schemas.rating_schemas import RatingModel

DICT_WITH_STARS = {"one_star": 1, "two_stars": 2, "three_stars": 3, "four_srats": 4, "five_stars": 5}


async def get_average_rating(image_id, db: Session):
    ratings = db.query(Rating).filter(Rating.image_id == image_id).all()
    if len(ratings) == 0:
        return 0
    sum_user_rating = 0
    for element in ratings:
        for key, value in element.items():
            if value:
                sum_user_rating += DICT_WITH_STARS[key]
    average_user_rating = sum_user_rating / len(ratings)
    return average_user_rating


async def get_rating(rating_id: int, db: Session) -> Rating:
    return db.query(Rating).filter(Rating.id == rating_id).first()


async def create_rating_from_user(image_id, body: RatingModel, user: User, db: Session) -> Rating | None:
    if user.id == body.user_id:
        return None
    rating_in_database = db.query(Rating).filter(Rating.image_id == image_id, Rating.user_id ==  body.user_id).first()
    if rating_in_database:
        return None
    rating_from_user = Rating(rating=body.rating.dict())
    db.add(rating_from_user)
    db.commit()
    db.refresh(rating_from_user)
    return rating_from_user



async def update_rating(rating_id: int, body: RatingModel, db: Session) -> Rating | None:
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        rating.rating = body.rating.dict()
        db.commit()
    return rating



async def remove_rating(rating_id: int, db: Session)  -> Rating | None:
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        db.delete(rating)
        db.commit()
    return rating


