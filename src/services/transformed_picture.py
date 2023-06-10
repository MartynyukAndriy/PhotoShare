# to install
# poetry add "qrcode[pil]"
# poetry add cloudinary

import io
import qrcode
from PIL import Image

import cloudinary
import cloudinary.uploader
from src.conf.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)


def upload_image(image_url: str):
    response = cloudinary.uploader.upload(image_url)
    return response


def get_url(image_url: str):
    return cloudinary.CloudinaryImage(image_url).build_url()


def get_transformed_url(image_url: str, transform_list: list[dict]):
    url = upload_image(image_url)
    return cloudinary.CloudinaryImage(url.get('url')).build_url(transformation=transform_list)


# Генеруємо QR-код "на лeту", без збереження на сервері:
def create_qrcode(image_url):
    # Creating the object QR-code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(image_url)
    qr.make(fit=True)

    # Creating the QR-code in memory
    img = qr.make_image(fill_color="black", back_color="white")
    image_stream = io.BytesIO()
    img.save(image_stream, format="PNG")
    image_stream.seek(0)

    # show image
    qr_image = Image.open(image_stream)
    return qr_image.show()


if __name__ == "__main__":
    upload_image('Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg')
    # result = get_url('marble_2.jpg')

  
    transformations = [
    {"width": 500, "height": 500, "crop": "fill"},
    {"effect": "grayscale"},
    {"angle": 90}
]
    result = get_transformed_url(
        get_url('Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg'), 
        transformation=transformations)
    create_qrcode(result)

    # create_qrcode('https://zrade.net/p/putin-khuilo-5mTx1EG63uPVNe2UU61W62')
