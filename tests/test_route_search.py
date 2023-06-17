import asyncio
import unittest
from unittest.mock import MagicMock, AsyncMock

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.routes.search import get_image_by_user_id, search_images_by_tag
from src.repository.search import get_img_by_user_id

from src.schemas.image_schemas import ImageDb
from src.database.models import User, Image
from datetime import datetime


class TestSearchRoutes(unittest.IsolatedAsyncioTestCase):
    def mock_get_img_by_user_id(self, user_id, db, current_user):
        if user_id == 1:
            return [
                ImageDb(id=1, url="image1.jpg", tags=[{"name": "tag1"}, {"name": "tag2"}], description="Image 1",
                        user_id=1, created_at=datetime(2022, 1, 1)),
                ImageDb(id=2, url="image2.jpg", tags=[{"name": "tag2"}, {"name": "tag3"}], description="Image 2",
                        user_id=1, created_at=datetime(2022, 1, 2)),
            ]
        else:
            raise ValueError("Only admin and moderator can get this data")

    async def test_get_image_by_user_id(self):
        user_id = 1
        db = Session()
        current_user = User(id=1)
        expected_images = [
            ImageDb(id=1, url="image1.jpg", tags=[{"name": "tag1"}, {"name": "tag2"}], description="Image 1", user_id=1,
                    created_at=datetime(2022, 1, 1)),
            ImageDb(id=2, url="image2.jpg", tags=[{"name": "tag2"}, {"name": "tag3"}], description="Image 2", user_id=1,
                    created_at=datetime(2022, 1, 2)),
        ]
        result = self.mock_get_img_by_user_id(user_id, db, current_user)
        self.assertEqual(result, expected_images)

    async def test_get_image_by_user_id_invalid_user_id(self):
        user_id = -1  # wrong user_id
        db = Session()
        current_user = User(id=1)

        with self.assertRaises(HTTPException) as context:
            await get_image_by_user_id(user_id, db, current_user)
        self.assertEqual(context.exception.status_code, 403)
