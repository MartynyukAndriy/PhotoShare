# poetry add "qrcode[pil]"
# poetry add cloudinary

import io
import qrcode
from PIL import Image
import cloudinary.uploader

from src.conf.config import settings
from src.schemas.transformed_image_schemas import TransformedImageModel

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)


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


def create_transformations(body: TransformedImageModel):
    transformations = []

    if body.resize:
        transform_set = {}
        mod_dict = body.resize.dict()
        print(mod_dict)
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
