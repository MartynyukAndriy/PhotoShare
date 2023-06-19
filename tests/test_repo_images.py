import unittest
from datetime import datetime
from unittest.mock import MagicMock

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Image, User, Tag, Comment, Role
from src.repository.images import delete_image, add_tag, update_image, add_image, admin_get_image, get_image, get_images
from src.repository.ratings import get_average_rating
from src.schemas.image_schemas import ImageUpdateModel, ImageAddModel, ImageAddTagModel
from src.services.images import images_service_normalize_tags


class TestImagesService(unittest.TestCase):
    def setUp(self):
        # Create a mock database session for testing
        self.db = MagicMock(spec=Session)
        self.user = User(id=1, role=Role.user)  # Create a mock user
        self.image = MagicMock()
        self.tags = ['tag1', 'tag2']
        self.db_tag = MagicMock()
        self.url = 'https://test.jpg'
        self.public_name = 'Test Image'
        self.user.id = 1
        self.image_id = 1
        self.body = MagicMock()

    async def test_get_images(self):
        # Mock the behavior of the get_average_rating function
        get_average_rating = MagicMock()
        get_average_rating.return_value = 4.5
        get_average_rating.attach_mock(
            MagicMock(return_value=[Comment(id=1, user_id=1, image_id=1, text='Nice image')]), 'return_value')

        # Mock the query method of the database session
        self.db.query.return_value.order_by.return_value.all.return_value = [
            Image(id=1, description='Test Image 1', user_id=1),
            Image(id=2, description='Test Image 2', user_id=2)
        ]

        expected_response = [
            {
                'image': Image(id=1, description='Test Image 1', user_id=1),
                'ratings': 4.5,
                'comments': [Comment(id=1, user_id=1, image_id=1, text='Nice image')]
            }
        ]

        result = await get_images(self.db, self.user)
        self.assertEqual(result, expected_response)

    async def test_get_image(self):
        # Mock the behavior of the get_average_rating function
        get_average_rating = MagicMock()
        get_average_rating.return_value = 4.2
        get_average_rating.attach_mock(
            MagicMock(return_value=[Comment(id=1, user_id=1, image_id=1, text='Nice image')]), 'return_value')

        # Mock the query method of the database session
        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, description='Test Image 1',
                                                                                  user_id=1)

        expected_result = (
            Image(id=1, description='Test Image 1', user_id=1),
            4.2,
            [Comment(id=1, user_id=1, image_id=1, text='Nice image')]
        )

        result = await get_image(self.db, 1, self.user)
        self.assertEqual(result, expected_result)

    async def test_admin_get_image(self):
        # Mock the behavior of the get_average_rating function
        get_average_rating = MagicMock()
        get_average_rating.return_value = 3.8
        get_average_rating.attach_mock(
            MagicMock(return_value=[Comment(id=2, user_id=1, image_id=2, text='Great picture')]), 'return_value')

        # Mock the query method of the database session
        self.db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
            Image(id=1, description='Test Image 1', user_id=2),
            Image(id=2, description='Test Image 2', user_id=2)
        ]

        expected_response = [
            {
                'image': Image(id=1, description='Test Image 1', user_id=2),
                'ratings': 3.8,
                'comments': [Comment(id=2, user_id=1, image_id=2, text='Great picture')]
            }
        ]

        result = await admin_get_image(self.db, 2)
        self.assertEqual(result, expected_response)

    async def test_add_image(self):
        # Mock the query method of the database session
        self.db.query.return_value.filter.return_value.first.return_value = User(id=1)

        # Mock the add, commit, and refresh methods of the database session
        self.db.add.return_value = None
        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        expected_image = Image(id=1, description='Test Image', user_id=1)

        result = await add_image(self.db, ImageAddModel(description='Test Image'), ['tag1', 'tag2'], 'https://test.jpg',
                                 'Test Image', self.user)
        self.assertEqual(result[0], expected_image)

    async def test_add_image_with_tags_less_than_5(self):
        num_tags = 0
        image_tags = []
        detail = ""
        for tag in self.tags:
            if len(tag) > 25:
                tag = tag[:25]
            if not self.db.query.return_value.filter.return_value.first.return_value:
                self.db_tag.name = tag.lower()
                self.assertEqual(self.db.add.call_count, num_tags)
                self.assertEqual(self.db.commit.call_count, num_tags)
                self.assertEqual(self.db.refresh.call_count, num_tags)
            if num_tags < 5:
                image_tags.append(tag.lower())
            num_tags += 1

        if num_tags >= 5:
            detail = " But be attentive you can add only five tags to an image"

        expected_image = Image(id=1, description='Test Image', user_id=1)

        result = await add_image(self.db, self.image, self.tags, self.url, self.public_name, self.user)
        self.assertEqual(result[0], expected_image)
        self.assertEqual(result[1], detail)
        self.assertEqual(self.db.add.call_count, num_tags)
        self.assertEqual(self.db.commit.call_count, num_tags)
        self.assertEqual(self.db.refresh.call_count, 1)

    async def test_add_image_with_tags_greater_than_or_equal_to_5(self):
        num_tags = 0
        image_tags = []
        detail = ""
        for tag in self.tags:
            if len(tag) > 25:
                tag = tag[:25]
            if not self.db.query.return_value.filter.return_value.first.return_value:
                self.db_tag.name = tag.lower()
                self.assertEqual(self.db.add.call_count, num_tags)
                self.assertEqual(self.db.commit.call_count, num_tags)
                self.assertEqual(self.db.refresh.call_count, num_tags)
            if num_tags < 5:
                image_tags.append(tag.lower())
            num_tags += 1

        if num_tags >= 5:
            detail = " But be attentive you can add only five tags to an image"
        self.assertEqual(detail, " But be attentive you can add only five tags to an image")
        self.assertEqual(len(image_tags), 5)

    async def test_add_image_with_user_none(self):
        user = None
        result = add_image(self.db, self.image, self.tags, self.url, self.public_name, user)
        self.assertIsNone(result)

    async def test_update_image(self):
        # Mock the query method of the database session
        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, description='Old Description',
                                                                                  user_id=1)

        # Mock the commit and refresh methods of the database session
        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        expected_image = Image(id=1, description='New Description', user_id=1)

        result = await update_image(self.db, 1, ImageUpdateModel(description='New Description'), self.user)
        self.assertEqual(result, expected_image)

    async def test_add_tag(self):
        tags_mock = ['tag1', 'tag2', 'tag3']
        normalize_tags_mock = MagicMock(return_value=tags_mock)
        images_service_normalize_tags = normalize_tags_mock

        self.db.query.return_value.filter.return_value.first.return_value = None

        self.user.role = Role.admin

        expected_tags = [Tag(name=tag.lower()) for tag in tags_mock]
        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, user_id=1)

        expected_image = Image(id=1, user_id=1, updated_at=datetime.utcnow(), tags=expected_tags)

        result = await add_tag(self.db, self.image_id, self.body, self.user)

        self.assertEqual(result[0], expected_image)
        self.assertEqual(result[1], "")
        self.assertEqual(self.db.commit.call_count, 1)
        self.assertEqual(self.db.refresh.call_count, 1)

        normalize_tags_mock.assert_called_once_with(self.body)

    async def test_add_tag_with_existing_image(self):
        tags_mock = ['tag1', 'tag2', 'tag3']
        normalize_tags_mock = MagicMock(return_value=tags_mock)
        images_service_normalize_tags = normalize_tags_mock

        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, user_id=1)

        expected_tags = [Tag(name=tag.lower()) for tag in tags_mock]

        expected_image = Image(id=1, user_id=1, updated_at=datetime.utcnow(), tags=expected_tags)

        result = await add_tag(self.db, self.image_id, self.body, self.user)

        self.assertEqual(result[0], expected_image)
        self.assertEqual(result[1], "")
        self.assertEqual(self.db.commit.call_count, 1)
        self.assertEqual(self.db.refresh.call_count, 1)

        normalize_tags_mock.assert_called_once_with(self.body)

    async def test_add_tag_with_user_id_mismatch(self):
        tags_mock = ['tag1', 'tag2', 'tag3']
        normalize_tags_mock = MagicMock(return_value=tags_mock)
        images_service_normalize_tags = normalize_tags_mock

        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, user_id=2)

        self.user.role = Role.user

        with self.assertRaises(HTTPException):
            await add_tag(self.db, self.image_id, self.body, self.user)

        normalize_tags_mock.assert_called_once_with(self.body)

    async def test_delete_image(self):
        # Mock the query method of the database session
        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, user_id=1)

        # Mock the delete, commit methods of the database session
        self.db.delete.return_value = None
        self.db.commit.return_value = None

        expected_image = Image(id=1, user_id=1)

        result = await delete_image(self.db, 1, self.user)
        self.assertEqual(result, expected_image)


if __name__ == '__main__':
    unittest.main()
