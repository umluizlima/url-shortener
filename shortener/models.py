from hashlib import md5

from django.core.validators import URLValidator
from django.db import models


class URL(models.Model):
    long_url = models.URLField(null=False)
    hashed_url = models.SlugField(max_length=200, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def _shorten(long_url: str) -> str:
        return md5(long_url.encode()).hexdigest()[:9]

    @staticmethod
    def _validate(long_url: str):
        validate = URLValidator()
        validate(long_url)

    def save(self, *args, **kwargs):
        self._validate(self.long_url)
        if not self.id:
            self.hashed_url = self._shorten(self.long_url)
        return super().save(*args, **kwargs)
