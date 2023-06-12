from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_


from src.database.models import Rating, User, Image
from src.schemas.rating_schemas import RatingModel


async def get_average_rating(image_id, db: Session):
    image_ratings = db.query(Rating).filter(Rating.image_id == image_id).all()
    if len(image_ratings) == 0:
        return 0
    sum_user_rating = 0
    for element in image_ratings:
        if element.one_star:
            sum_user_rating += 1
        if element.two_stars:
            sum_user_rating += 2
        if element.three_stars:
            sum_user_rating += 3
        if element.four_stars:
            sum_user_rating += 4
        if element.five_stars:
            sum_user_rating += 5
    average_user_rating = sum_user_rating / len(image_ratings)
    return average_user_rating


async def get_rating(rating_id: int, db: Session) -> Rating:
    return db.query(Rating).filter(Rating.id == rating_id).first()


async def create_rating(image_id: int, body: RatingModel, user: User, db: Session) -> Rating:
    image_in_database = db.query(Image).filter(Image.id == image_id).first()
    if image_in_database.user_id == user.id:
        return None
    sum_of_rates = 0
    for el in body:
        if el[1]:
            sum_of_rates += 1
    if sum_of_rates > 1:
        return None
    rating_in_database = db.query(Rating).filter(Rating.image_id == image_id, Rating.user_id == user.id).first()
    if rating_in_database:
        return rating_in_database
    rating = Rating(one_star=body.one_star, two_stars=body.two_stars, three_stars=body.three_stars, user_id=user.id, image_id=image_id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


async def update_rating(rating_id: int, body: RatingModel, db: Session):
    sum_of_rates = 0
    for el in body:
        if el[1]:
            sum_of_rates += 1
    if sum_of_rates > 1:
        return None
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        rating.one_star = body.one_star
        rating.two_stars = body.two_stars
        rating.three_stars = body.three_stars
        rating.four_stars = body.four_stars
        rating.five_stars = body.five_stars
        db.commit()
    return rating


async def remove_rating(rating_id: int, db: Session):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        db.delete(rating)
        db.commit()
    return rating
