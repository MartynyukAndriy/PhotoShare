import unittest

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Rating, Base
from src.repository.search import calc_average_rating


class CalcAverageRatingTestCase(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.db = Session()

    def tearDown(self):
        # Close the database session and drop all tables
        self.db.close_all()
        Base.metadata.drop_all(bind=self.db.bind)

    def test_average_rating_no_ratings(self):
        # Test case for image with no ratings
        image_id = 1

        average_rating = calc_average_rating(image_id, self.db)

        self.assertEqual(average_rating, 0)

    def test_average_rating_single_rating(self):
        # Test case for image with one rating
        image_id = 1
        rating = Rating(image_id=image_id, one_star=False, two_stars=False,
                        three_stars=False, four_stars=False, five_stars=True)
        self.db.add(rating)
        self.db.commit()

        average_rating = calc_average_rating(image_id, self.db)

        self.assertEqual(average_rating, 5)

    def test_average_rating_multiple_ratings(self):
        # Test case for image with multiple ratings
        image_id = 1
        ratings = [
            Rating(image_id=image_id, one_star=False, two_stars=True,
                   three_stars=False, four_stars=False, five_stars=False),
            Rating(image_id=image_id, one_star=False, two_stars=False,
                   three_stars=False, four_stars=True, five_stars=False),
            Rating(image_id=image_id, one_star=False, two_stars=False,
                   three_stars=False, four_stars=False, five_stars=True)
        ]
        self.db.add_all(ratings)
        self.db.commit()

        average_rating = calc_average_rating(image_id, self.db)

        self.assertAlmostEqual(average_rating, 3.6666666666666665, places=6)

    def test_average_rating_duplicate_stars(self):
        # Test case for image with multiple ratings and duplicate stars
        image_id = 1
        ratings = [
            Rating(image_id=image_id, one_star=False, two_stars=False,
                   three_stars=True, four_stars=False, five_stars=False),
            Rating(image_id=image_id, one_star=False, two_stars=False,
                   three_stars=True, four_stars=False, five_stars=False),
            Rating(image_id=image_id, one_star=False, two_stars=False,
                   three_stars=False, four_stars=True, five_stars=False),
            Rating(image_id=image_id, one_star=False, two_stars=False,
                   three_stars=False, four_stars=True, five_stars=False),
            Rating(image_id=image_id, one_star=False, two_stars=False,
                   three_stars=False, four_stars=False, five_stars=True)
        ]
        self.db.add_all(ratings)
        self.db.commit()

        average_rating = calc_average_rating(image_id, self.db)

        self.assertAlmostEqual(average_rating, 3.8, places=6)

    def test_average_rating_nonexistent_image(self):
        # Test case for non-existent image
        image_id = 999

        average_rating = calc_average_rating(image_id, self.db)

        self.assertEqual(average_rating, 0)




# ============================

import unittest
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Image, User, Tag, Rating, image_m2m_tag, Role
from src.repository.search import get_img_by_user_id

class GetImageByUserIdTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Create an in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.db = Session()

    async def asyncTearDown(self):
        # Close the database session and drop all tables
        self.db.close_all()
        Base.metadata.drop_all(bind=self.db.bind)

    async def test_get_img_by_user_id_sort_by_date_descending(self):
        # Test case for sorting images by date in descending order
        user_id = 1
        skip = 0
        limit = 10
        filter_type = "d"
        user = User(role=Role.admin)  # User with admin role

        try:
            await get_img_by_user_id(user_id, skip, limit, filter_type, self.db, user)
        except HTTPException as e:
            self.assertEqual(e.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(e.detail, "Images for this user not found")

    @unittest.skip
    async def test_get_img_by_user_id_sort_by_date_ascending(self):
        # Test case for sorting images by date in ascending order
        user_id = 1
        skip = 0
        limit = 10
        filter_type = "-d"
        user = User(role=Role.moderator)  # User with moderator role

        # TODO: Add test data to the database for the given scenario

        images = await get_img_by_user_id(user_id, skip, limit, filter_type, self.db, user)

        # TODO: Add assertions to verify the correctness of the results

    async def test_get_img_by_user_id_unauthorized_user(self):
        # Test case for an unauthorized user
        user_id = 1
        skip = 0
        limit = 10
        filter_type = "d"
        user = User(role=Role.user)  # User with user role (no access)

        with self.assertRaises(HTTPException) as cm:
            await get_img_by_user_id(user_id, skip, limit, filter_type, self.db, user)

        self.assertEqual(cm.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(cm.exception.detail, "Only admin or moderator can get this data")

    # Other test cases...

if __name__ == '__main__':
    unittest.main()