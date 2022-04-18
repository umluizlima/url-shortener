from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import URL


class URLModelTests(TestCase):
    def test_url_is_shortened_on_save(self):
        long_url = "https://google.com"
        short_url = URL._shorten(long_url)
        url = URL(long_url=long_url)
        url.save()
        self.assertEqual(url.hashed_url, short_url)

    def test_rejects_invalid_url(self):
        long_url = "google"
        url = URL(long_url=long_url)
        self.assertRaises(ValidationError, url.save)
