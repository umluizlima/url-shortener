from django.db import models


class URL(models.Model):
    long_url = models.URLField(null=False)
    hashed_url = models.CharField(max_length=200, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
