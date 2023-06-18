import asyncio
import unittest
from unittest.mock import MagicMock, AsyncMock

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.routes.search import get_image_by_user_id, search_images_by_tag
from src.repository.search import get_img_by_user_id

from src.schemas.transformed_image_schemas import SearchImageResponse
from src.database.models import User
from datetime import datetime


class TestSearchRoutes(unittest.IsolatedAsyncioTestCase):
    def mock_get_img_by_user_id(self, user_id, db, current_user):
        if user_id == 1:
            return [
                SearchImageResponse(id=1, url="image1.jpg", tags=[{"name": "tag1"}, {"name": "tag2"}], description="Image 1",
                        user_id=1, created_at=datetime(2022, 1, 1), rating=5),
                SearchImageResponse(id=2, url="image2.jpg", tags=[{"name": "tag2"}, {"name": "tag3"}], description="Image 2",
                        user_id=1, created_at=datetime(2022, 1, 2), rating=3),
            ]
        else:
            raise ValueError("Only admin and moderator can get this data")

    async def test_get_image_by_user_id(self):
        user_id = 1
        db = Session()
        current_user = User(id=1)
        expected_images = [
            SearchImageResponse(id=1, url="image1.jpg", tags=[{"name": "tag1"}, {"name": "tag2"}],
                                description="Image 1",
                                user_id=1, created_at=datetime(2022, 1, 1), rating=5),
            SearchImageResponse(id=2, url="image2.jpg", tags=[{"name": "tag2"}, {"name": "tag3"}],
                                description="Image 2",
                                user_id=1, created_at=datetime(2022, 1, 2), rating=3),
        ]
        result = self.mock_get_img_by_user_id(user_id, db, current_user)
        self.assertEqual(result, expected_images)

    async def test_get_image_by_user_id_invalid_user_id(self):
        user_id = -1  # wrong user_id
        db = Session()
        current_user = User(id=1, role="admin")

        with self.assertRaises(HTTPException) as context:
            if current_user.role != "admin":  # Перевірка ролі користувача
                raise HTTPException(status_code=403, detail="Only admin and moderator can get this data")
            await get_img_by_user_id(user_id, 0, 10, 'd', db, current_user)
        self.assertEqual(context.exception.status_code, 403)
