from typing import Optional
from pydantic import BaseModel


class RatingModel(BaseModel):
    one_star: Optional[bool] = False
    two_stars: Optional[bool] = False
    three_stars: Optional[bool] = False
    four_stars: Optional[bool] = False
    five_stars: Optional[bool] = False

class RatingResponse(RatingModel):
    id: int = 1
    one_star: bool = False
    two_stars: bool = False
    three_stars: bool = False
    four_stars: bool = False
    five_stars: bool = False
    user_id: int = 1
    image_id: int = 1

    class Config:
        orm_mode = True


class AverageRatingResponse(RatingModel):
    avarage_rating: float = 0.0
 
    class Config:
        orm_mode = True
