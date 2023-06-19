import unittest
from datetime import datetime
from io import BytesIO
from unittest.mock import MagicMock

from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.database.models import Image, User, Tag, Comment, Role
from src.repository.ratings import get_average_rating
from src.routes.images import upload_image
from src.schemas.image_schemas import ImageUpdateModel, ImageAddModel, ImageAddTagModel
from src.services.images import images_service_normalize_tags
from src.routes import images


class TestImagesRoute(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)

        # Creating a mock user with admin role
        self.admin_user = User(id=1, role=Role.admin)
        self.non_admin_user = User(id=2, role=Role.user)

        # Creating mock image objects
        self.image1 = Image(id=1, user_id=1)
        self.image2 = Image(id=2, user_id=2)

        # Creating mock comment objects
        self.comment1 = Comment(id=1, user_id=1, image_id=1)
        self.comment2 = Comment(id=2, user_id=2, image_id=2)

        # Creating mock tag objects
        self.tag1 = Tag(id=1, name='tag1')
        self.tag2 = Tag(id=2, name='tag2')

        self.current_user = User(id=1, username='testuser')
        self.body = MagicMock()
        self.file = UploadFile(filename='test.jpg', file=MagicMock())

    async def test_get_image_as_admin(self):
        # Mocking the query and return values
        self.db.query.return_value.filter.return_value.first.return_value = self.image1
        get_average_rating_mock = self.db.get_average_rating = MagicMock(return_value=5)
        self.db.query.return_value.filter.return_value.all.return_value = [self.comment1]

        # Calling the function
        result = await images.get_image(1, self.db, self.admin_user)

        # Asserting the expected values
        self.assertEqual(result, (self.image1, 5, [self.comment1]))
        get_average_rating_mock.assert_called_once_with(1, self.db)

    async def test_get_image_as_user(self):
        # Mocking the query and return values
        self.db.query.return_value.filter.return_value.first.return_value = self.image2
        get_average_rating_mock = self.db.get_average_rating = MagicMock(return_value=4)
        self.db.query.return_value.filter.return_value.all.return_value = [self.comment2]

        # Calling the function
        result = await images.get_image(2, self.db, self.non_admin_user)

        # Asserting the expected values
        self.assertEqual(result, (self.image2, 4, [self.comment2]))
        get_average_rating_mock.assert_called_once_with(2, self.db)

    async def test_get_image_image_not_found(self):
        # Mocking the query and return values
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Calling the function
        with self.assertRaises(Exception) as context:
            await images.get_image(1, self.db, self.non_admin_user)

        # Asserting the expected exception
        self.assertEqual(context.exception.args[0], "Image not found")

    async def test_admin_get_image(self):
        # Mocking the query and return values
        self.db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [self.image1,
                                                                                                 self.image2]
        get_average_rating_mock = self.db.get_average_rating = MagicMock(return_value=5)
        self.db.query.return_value.filter.return_value.all.return_value = [self.comment1, self.comment2]

        # Calling the function
        result = await images.admin_get_images(1, self.db, self.admin_user)

        # Asserting the expected values
        self.assertEqual(result, [
            {"image": self.image1, "ratings": 5, "comments": [self.comment1]},
            {"image": self.image2, "ratings": 5, "comments": [self.comment2]}
        ])
        get_average_rating_mock.assert_called_with(self.image1.id, self.db)
        get_average_rating_mock.assert_called_with(self.image2.id, self.db)

    async def test_upload_image(self):
        normalize_tags_mock = MagicMock(return_value=['tag1', 'tag2', 'tag3'])
        change_name_mock = MagicMock(return_value='correct_name')
        images_service_normalize_tags = normalize_tags_mock
        images_service_change_name = change_name_mock

        expected_image = MagicMock()

        images_mock = MagicMock()
        images_mock.add_image.return_value = (expected_image, 'details')

        with unittest.mock.patch('app.main.images', images_mock):
            result = await upload_image(self.body, self.file, self.db, self.current_user)

        self.assertEqual(result['image'], expected_image)
        self.assertEqual(result['detail'], 'Image was successfully added.details')

        normalize_tags_mock.assert_called_once_with(self.body)
        change_name_mock.assert_called_once_with('test', self.db)
        images_mock.add_image.assert_called_once_with(self.db, self.body, ['tag1', 'tag2', 'tag3'],
                                                      'src_url', 'correct_name', self.current_user)

    async def test_update_image_image_not_found(self):
        # Mocking the query and return values
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Creating mock input data
        image_update_model = ImageUpdateModel(description='Updated description')

        # Calling the function
        with self.assertRaises(Exception) as context:
            await images.update_description(1, image_update_model, self.db, self.admin_user)

        # Asserting the expected exception
        self.assertEqual(context.exception.args[0], "Image not found")
        self.db.query.return_value.filter.assert_called_with(Image.id == 1)
        self.db.commit.assert_not_called()
        self.db.refresh.assert_not_called()

    async def test_add_image_missing_description(self):
        # Mocking the query and return values
        self.db.query.return_value.filter.return_value.first.return_value = None
        self.db.query.return_value.filter.return_value.all.return_value = [self.tag1, self.tag2]
        self.db.add.return_value = None
        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        # Creating mock input data without description
        image_add_model = ImageAddModel(description='', tags=['tag1', 'tag2'])
        file_data = b"file content"
        file = UploadFile(filename="test.txt", file=BytesIO(file_data))

        # Calling the function
        result = await images.upload_image(image_add_model, file, self.db, self.admin_user)

        # Asserting the expected values
        self.assertIsNone(result[0])
        self.assertEqual(result[1], "Description is required.")
        self.db.query.return_value.filter.assert_not_called()
        self.db.add.assert_not_called()
        self.db.commit.assert_not_called()
        self.db.refresh.assert_not_called()

    async def test_update_image(self):
        # Mocking the query and return values
        self.db.query.return_value.filter.return_value.first.return_value = self.image1
        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        # Creating mock input data
        image_update_model = ImageUpdateModel(description='Updated description')

        # Calling the function
        result = await images.update_description(1, image_update_model, self.db, self.admin_user)

        # Asserting the expected values
        self.assertEqual(result.description, 'Updated description')
        self.db.query.return_value.filter.assert_called_with(Image.id == 1)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_with(self.image1)

    async def test_add_tag(self):
        # Mocking the query and return values
        self.db.query.return_value.filter.return_value.first.return_value = self.image1
        self.db.query.return_value.filter.return_value.all.return_value = [self.tag1, self.tag2]
        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        # Creating mock input data
        image_add_tag_model = ImageAddTagModel(tags=['tag1', 'tag2'])

        # Calling the function
        result = await images.add_tag(1, image_add_tag_model, self.db, self.admin_user)

        # Asserting the expected values
        self.assertEqual(result, self.image1)
        self.db.query.return_value.filter.assert_called_with(Tag.name.in_(['tag1', 'tag2']))
        self.db.query.return_value.filter.assert_called_with(Image.id == 1)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_with(self.image1)

    async def test_delete_image(self):
        # Mocking the query and return values
        self.db.query.return_value.filter.return_value.first.return_value = self.image1
        self.db.delete.return_value = None
        self.db.commit.return_value = None

        # Calling the function
        result = await images.delete_image(1, self.db, self.admin_user)

        # Asserting the expected values
        self.assertEqual(result, self.image1)
        self.db.query.return_value.filter.assert_called_with(Image.id == 1)
        self.db.delete.assert_called_with(self.image1)
        self.db.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
