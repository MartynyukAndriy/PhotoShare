import unittest
from unittest.mock import patch
from PIL import Image
from src.schemas.transformed_image_schemas import TransformedImageModel
from src.services.transformed_image import generate_and_upload_qr_code, create_transformations


class TestCreateQRCode(unittest.TestCase):
    @patch("PIL.Image.Image.show")
    def test_create_qrcode(self, mock_show):
        image_url = "https://example.com/image.jpg"
        qr_image = generate_and_upload_qr_code(image_url)
        mock_show.assert_called_once()

class TestCreateTransformations(unittest.TestCase):
    def test_create_transformations(self):
        body = TransformedImageModel(
            resize={
                "width": 800,
                "height": 600
            },
            radius={
                "max": True
            },
            rotate={
                "degree": 90
            }
        )

        transformations = create_transformations(body)
        self.assertEqual(len(transformations), 3)

        expected_transformations = [
            {'gravity': 'auto', 'width': 800, 'height': 600},
            {'radius': 'max'},
            {'angle': 90},
        ]
        self.assertEqual(transformations, expected_transformations)
