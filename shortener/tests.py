from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

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


def create_url(long_url: str):
    return URL.objects.create(long_url=long_url)


class URLRedirectViewTests(TestCase):
    def test_hash_not_found(self):
        response = self.client.get(reverse("shortener:redirect", args=("abc",)))
        self.assertEqual(response.status_code, 404)

    def test_hash_redirects_to_url(self):
        url = create_url("https://google.com")
        response = self.client.get(
            reverse("shortener:redirect", args=(url.hashed_url,))
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url.long_url)

    def test_hash_redirects_to_correct_url(self):
        url = create_url("https://google.com")
        create_url("https://github.com")
        response = self.client.get(
            reverse("shortener:redirect", args=(url.hashed_url,))
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url.long_url)
