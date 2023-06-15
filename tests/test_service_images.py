import unittest
import asyncio
from unittest.mock import Mock
from src.database.models import Image
from src.services.images import images_service_change_name, images_service_normalize_tags
from src.schemas.image_schemas import ImageAddModel


class TestImagesService(unittest.TestCase):

    def test_images_service_change_name(self):
        async def test_async_images_service_change_name():
            db_mock = Mock()
            db_mock.query.return_value.filter.return_value.first.return_value = None

            public_name = "test_image"
            new_name = await images_service_change_name(public_name, db_mock)

            self.assertEqual(new_name, public_name)

        asyncio.run(test_async_images_service_change_name())

    def test_normalize_tags(self):
        async def test_async_normalize_tags():
            tags = ["tag1, tag2, tag3", "tag1, tag4, tag5", "tag5"]
            description = "film"
            body = ImageAddModel(tags=tags, description=description)
            correct_tags = await images_service_normalize_tags(body)

            expected_correct_tags = ["tag1", "tag2", "tag3", "tag4", "tag5"]
            self.assertEqual(correct_tags, expected_correct_tags)

        asyncio.run(test_async_normalize_tags())


if __name__ == '__main__':
    unittest.main()
