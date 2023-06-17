import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.routes.search import get_image_by_user_id, search_images_by_tag
from src.database.models import User
from src.schemas.image_schemas import ImageDb


class TestSearchRepository(unittest.IsolatedAsyncioTestCase):
    async def test_get_image_by_user_id(self):

        user_id = 1
        db = MagicMock(spec=Session)
        current_user = User(id=1)
        expected_images = [
            ImageDb(id=1, url="image1.jpg", tags=["tag1", "tag2"]),
            ImageDb(id=2, url="image2.jpg", tags=["tag3"]),
        ]

        async def mock_get_img_by_user_id(user_id, db, current_user):
            return expected_images

        result = await get_image_by_user_id(user_id, db, current_user, get_img_by_user_id=mock_get_img_by_user_id)
        self.assertEqual(result, expected_images)

    async def test_get_image_by_user_id_invalid_user_id(self):
        user_id = 0  # Invalid user_id
        db = MagicMock(spec=Session)
        current_user = User(id=1)

        async def mock_get_img_by_user_id(user_id, db, current_user):
            return [
                ImageDb(id=1, url="image1.jpg", tags=["tag1", "tag2"]),
                ImageDb(id=2, url="image2.jpg", tags=["tag3"]),
            ]

        with self.assertRaises(HTTPException):
            await get_image_by_user_id(user_id, db, current_user, get_img_by_user_id=mock_get_img_by_user_id)

    async def test_search_images_by_tag(self):
        # Arrange
        skip = 0
        limit = 10
        search_tag = "tag1"
        filter_type = "d"
        db = MagicMock(spec=Session)
        user = User(id=1)
        expected_images = [
            ImageDb(id=1, url="image1.jpg", tags=["tag1", "tag2"]),
            ImageDb(id=2, url="image2.jpg", tags=["tag3"]),
        ]

        def mock_find_image_by_tag(skip, limit, search_tag, filter_type, db, user):
            return expected_images

        result = await search_images_by_tag(skip, limit, search_tag, filter_type, db, user, find_image_by_tag=mock_find_image_by_tag)
        self.assertEqual(result, expected_images)

    async def test_search_images_by_tag_no_results(self):
        skip = 0
        limit = 10
        search_tag = "tag4"  # Non-existent tag
        filter_type = "d"
        db = MagicMock(spec=Session)
        user = User(id=1)

        def mock_find_image_by_tag(skip, limit, search_tag, filter_type, db, user):
            return []

        result = await search_images_by_tag(skip, limit, search_tag, filter_type, db, user, find_image_by_tag=mock_find_image_by_tag)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
