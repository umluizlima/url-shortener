from django.core.validators import URLValidator
from django.db import models

from .utils import generate_hash


class URL(models.Model):
    long_url = models.URLField(null=False)
    hashed_url = models.SlugField(max_length=200, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.long_url} - {self.hashed_url}"

    @staticmethod
    def _validate(long_url: str):
        validate = URLValidator()
        validate(long_url)

    def save(self, *args, **kwargs):
        self._validate(self.long_url)
        if not self.id:
            self.hashed_url = generate_hash()
        return super().save(*args, **kwargs)
