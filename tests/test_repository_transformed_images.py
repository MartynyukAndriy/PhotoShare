import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.database.models import TransformedImage, Image, User, Role
from src.schemas.transformed_image_schemas import TransformedImageModel
from src.repository.transformed_images import create_transformed_picture, get_all_transformed_images, \
    get_transformed_img_by_id, delete_transformed_image_by_id, get_qrcode_transformed_image_by_id, \
    get_url_transformed_image_by_id, get_transformed_img_by_user_id


class TestTransformedImageRepository(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_db = MagicMock(spec=Session)
        self.mock_current_user = MagicMock(spec=User)
        self.mock_original_image = MagicMock(spec=Image)
        self.mock_transformed_image = MagicMock(spec=TransformedImage)
        self.mock_body = TransformedImageModel()
        self.mock_image_id = 1
        self.mock_transformed_id = 1

    async def test_create_transformed_picture_success(self):
        # переконуємося, що функція повертає створений об'єкт TransformedImage
        self.mock_db.query.filter.first.return_value = self.mock_original_image
        self.mock_original_image.public_name = "public_name"
        self.mock_original_image.id = 1
        self.mock_current_user.id = 1
        result = await create_transformed_picture(self.mock_body, self.mock_current_user, self.mock_image_id,
                                                  self.mock_db)
        self.assertIsInstance(result, TransformedImage)

    async def test_create_transformed_picture_original_image_not_found(self):
        # Переконуємося що функція викликає виключення HTTPException, якщо оригінальне зображення не знайдено
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        with self.assertRaises(HTTPException) as context:
            await create_transformed_picture(self.mock_body, self.mock_current_user, self.mock_image_id, self.mock_db)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    async def test_get_all_transformed_images_success(self):
        # Переконуємося, що функція повертає список TransformedImage
        self.mock_db.query.return_value.join.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [
            self.mock_transformed_image]
        self.mock_current_user.id = 1
        result = await get_all_transformed_images(0, 10, self.mock_image_id, self.mock_db, self.mock_current_user)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], TransformedImage)

    async def test_get_all_transformed_images_not_found(self):
        # Переконуємося, що функція викликає виключення HTTPException, якщо трансформовані зображення не знайдені
        self.mock_db.query.return_value.join.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        self.mock_current_user.id = 1
        with self.assertRaises(HTTPException) as context:
            await get_all_transformed_images(0, 10, self.mock_image_id, self.mock_db, self.mock_current_user)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    async def test_get_transformed_img_by_id_success(self):
        # Переконуємося, що функція повертає об'єкт TransformedImage
        self.mock_db.query.return_value.join.return_value.filter.return_value.first.return_value = self.mock_transformed_image
        self.mock_current_user.id = 1
        result = await get_transformed_img_by_id(self.mock_transformed_id, self.mock_db, self.mock_current_user)
        self.assertIsInstance(result, TransformedImage)

    async def test_get_transformed_img_by_id_not_found(self):
        # Переконуємося, що функція викликає виключення HTTPException, якщо трансформовані зображення не знайдено
        self.mock_db.query.return_value.join.return_value.filter.return_value.first.return_value = None
        self.mock_current_user.id = 1
        with self.assertRaises(HTTPException) as context:
            await get_transformed_img_by_id(self.mock_transformed_id, self.mock_db, self.mock_current_user)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    async def test_delete_transformed_image_by_id_success(self):
        self.mock_db.query.return_value.join.return_value.filter.return_value.first.return_value = self.mock_transformed_image
        self.mock_current_user.id = 1
        self.mock_current_user.role = Role.admin
        result = await delete_transformed_image_by_id(self.mock_transformed_id, self.mock_db, self.mock_current_user)
        self.assertIsInstance(result, TransformedImage)

    async def test_delete_transformed_image_by_id_not_found(self):
        self.mock_db.query.return_value.join.return_value.filter.return_value.first.return_value = None
        self.mock_current_user.id = 1
        with self.assertRaises(HTTPException) as context:
            await delete_transformed_image_by_id(self.mock_transformed_id, self.mock_db, self.mock_current_user)
        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)

    async def test_get_qrcode_transformed_image_by_id_success(self):
        # Переконуємося, що функція повертає об'єкт TransformedImage
        self.mock_db.query.return_value.join.return_value.filter.return_value.first.return_value = self.mock_transformed_image
        self.mock_current_user.id = 1
        result = await get_qrcode_transformed_image_by_id(self.mock_transformed_id, self.mock_db,
                                                          self.mock_current_user)
        self.assertIsInstance(result, TransformedImage)

    async def test_get_qrcode_transformed_image_by_id_not_found(self):
        # Переконуємося, що функція викликає виключення HTTPException, якщо трансформовані зображення не знайдено
        self.mock_db.query.return_value.join.return_value.filter.return_value.first.return_value = None
        self.mock_current_user.id = 1
        with self.assertRaises(HTTPException) as context:
            await get_qrcode_transformed_image_by_id(self.mock_transformed_id, self.mock_db, self.mock_current_user)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    async def test_get_url_transformed_image_by_id_success(self):
        # переконуємося, що функція повертає об'єкт TransformedImage
        self.mock_db.query.return_value.join.return_value.filter.return_value.first.return_value = self.mock_transformed_image
        self.mock_current_user.id = 1
        result = await get_url_transformed_image_by_id(self.mock_transformed_id, self.mock_db, self.mock_current_user)
        self.assertIsInstance(result, TransformedImage)

    async def test_get_url_transformed_image_by_id_not_found(self):
        # переконуємося, що функція викликає виключення HTTPException, якщо трансформовані зображення не знайдено
        self.mock_db.query.return_value.join.return_value.filter.return_value.first.return_value = None
        self.mock_current_user.id = 1
        with self.assertRaises(HTTPException) as context:
            await get_url_transformed_image_by_id(self.mock_transformed_id, self.mock_db, self.mock_current_user)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    async def test_get_transformed_img_by_user_id_success(self):
        # переконуємося, що функція повертає список TransformedImage
        self.mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [
            self.mock_transformed_image]
        self.mock_current_user.id = 1
        result = await get_transformed_img_by_user_id(1, self.mock_db, self.mock_current_user)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], TransformedImage)

    async def test_get_transformed_img_by_user_id_not_found(self):
        # переконуємося, що функція викликає виключення HTTPException, якщо трансформовані зображення не знайдено
        self.mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []
        self.mock_current_user.id = 1
        with self.assertRaises(HTTPException) as context:
            await get_transformed_img_by_user_id(1, self.mock_db, self.mock_current_user)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()