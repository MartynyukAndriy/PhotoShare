import io
import qrcode
from PIL import Image


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
    create_qrcode('https://zrade.net/p/putin-khuilo-5mTx1EG63uPVNe2UU61W62')
