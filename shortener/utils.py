import random

from django.conf import settings


def generate_hash() -> str:
    return "".join(
        random.choices(settings.CONFIG.HASH_CHARACTERS, k=settings.CONFIG.HASH_LENGTH)
    )
