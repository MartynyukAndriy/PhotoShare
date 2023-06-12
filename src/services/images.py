from src.database.models import Image


async def images_service_change_name(public_name, db):
    correct_public_name = public_name
    suffix = 1

    while db.query(Image).filter(Image.public_name == correct_public_name).first():
        suffix += 1
        correct_public_name = f"{public_name}_{suffix}"

    return correct_public_name


async def images_service_id_exists(id, db):
    if db.query(Image).filter(Image.id == id).first():
        return True
    else:
        return False

