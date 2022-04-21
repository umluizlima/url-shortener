import random

from django.conf import settings


def generate_hash() -> str:
    return "".join(random.choices(settings.HASH_CHARACTERS, k=settings.HASH_LENGTH))
