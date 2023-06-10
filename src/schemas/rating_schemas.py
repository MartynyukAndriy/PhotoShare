from pydantic import BaseModel, Field
from typing import Dict

from user_schemas import UserResponse

class ViewRatingModel(BaseModel):
    one_star: bool
    two_stars: bool
    three_stars: bool
    four_stars: bool
    five_stars: bool

class RatingModel(BaseModel):
    rating: ViewRatingModel
    user_id: int = Field(1, gt=0)
    image_id: int = Field(1, gt=0)


class RatingResponse(BaseModel):
    id: int = 1
    rating: dict = {"one_star": False, "two_stars": False, "three_stars": False, "four_srats": False, "five_stars": False}
    user: UserResponse

    class Config:
        orm_mode = True

