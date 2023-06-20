import qrcode
import cloudinary
import cloudinary.uploader
import tempfile
import os
from src.schemas.transformed_image_schemas import TransformedImageModel
from src.conf.config import settings


def generate_and_upload_qr_code(url, box_size=6, border=2):
    """
    The generate_and_upload_qr_code function generates a QR code from the given URL and uploads it to Cloudinary.

    :param url: Pass the url of the page that will be encoded into a qr code
    :param box_size: Set the size of each box in the qr code
    :param border: Specify the width of the border around the qr code
    :return: A dictionary with the uploaded image url
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make()
    image = qr.make_image()

    # Створюємо тимчасову директорію, якщо вона не існує
    temp_dir = os.path.join(tempfile.gettempdir(), 'qr_codes')
    os.makedirs(temp_dir, exist_ok=True)

    # Створюємо унікальний файл з унікальним іменем
    temp_file_path = os.path.join(temp_dir, next(tempfile._get_candidate_names()) + '.png')
    image.save(temp_file_path)

    # Завантажуємо QR-код на Cloudinary
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    result = cloudinary.uploader.upload(temp_file_path)

    # Видаляємо тимчасовий файл
    os.remove(temp_file_path)

    return result['secure_url']


def create_transformations(body: TransformedImageModel):
    """ func create_transformations create list of transformations for images placed on Cloudinary"""

    transformations = []

    if body.resize:
        transform_set = {}
        mod_dict = body.resize.dict()
        for key in mod_dict:
            if mod_dict[key]:
                if type(mod_dict[key]) in (int, str):
                    transform_set[key] = mod_dict[key]
                elif isinstance(mod_dict[key], dict):
                    data = [key for key, value in mod_dict[key].items() if value]
                    transform_set[key] = data[0]
        transformations.append(transform_set)

    if body.radius:
        if body.radius.max:
            transformations.append({'radius': 'max'})
        elif body.radius.all > 0:
            transformations.append({'radius': body.radius.all})
        else:
            transformations.append({'radius': f'{body.radius.left_top}:{body.radius.right_top}:'
                                              f'{body.radius.right_bottom}:{body.radius.left_bottom}'})
    if body.rotate:
        transformations.append({'angle': body.rotate.degree})

    return transformations
