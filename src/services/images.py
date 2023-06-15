from fastapi import HTTPException, status

from src.database.models import Image
from src.schemas.image_schemas import ImageAddModel


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


async def images_service_normalize_tags(body):
    """
    The normalize_tags function takes a list of tags and returns a list of unique, non-empty tags.
        Args:
            body (list): A list of strings representing the tags to be normalized.

    :param body: Get the tags from the request body
    :return: A list of tags
    """
    correct_tags = []
    tags = []
    tags_set = set()
    for tag_str in body.tags:
        tags.extend(tag_str.split(","))
    tags = [tag.strip() for tag in tags]
    for tag in tags:
        if tag:
            tags_set.add(tag)
    if tags_set:
        for tag in tags:
            if tag in tags_set and tag not in correct_tags:
                correct_tags.append(tag)
    return correct_tags
