from fastapi import HTTPException, status

from src.database.models import Image


async def images_service_change_name(public_name, db):
    """
    The images_service_change_name function takes in a public_name and db.
    It then checks if the public_name is already taken by another image, and if it is, it adds a suffix to the end of
    the name until there are no more duplicates. It returns this new name.

    :param public_name: Check if the name is already in use
    :param db: Access the database
    :return: A name that is not used in the database
    """

    correct_public_name = public_name
    suffix = 1

    while db.query(Image).filter(Image.public_name == correct_public_name).first():
        suffix += 1
        correct_public_name = f"{public_name}_{suffix}"

    return correct_public_name


async def normalize_tags(body):
    """
    The normalize_tags function takes a list of tags and returns a new list.

    :param body: Get the request body
    :return: A list of tags

    """
    correct_tags = set()
    for tag_str in body.tags:
        tags = tag_str.split(",")
        for tag in tags:
            if tag:
                correct_tags.add(tag)

    correct_tags = list(correct_tags)
    if len(correct_tags) > 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Maximum of 5 tags allowed'
        )
    return correct_tags
