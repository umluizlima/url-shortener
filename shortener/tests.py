from unittest.mock import patch

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from shortener.models import URL
from shortener.utils import generate_hash


def mock_generate_hash():
    return "abcdef"


def create_url(long_url: str):
    return URL.objects.create(long_url=long_url)


class URLModelTests(TestCase):
    @patch("shortener.models.generate_hash", mock_generate_hash)
    def test_url_is_shortened_on_save(self):
        long_url = "https://google.com"
        short_url = mock_generate_hash()
        url = URL(long_url=long_url)
        url.save()
        self.assertEqual(url.hashed_url, short_url)

    @patch("shortener.models.generate_hash", mock_generate_hash)
    def test_raises_error_on_duplicate_hash(self):
        long_url = "https://google.com"
        create_url(long_url)
        url = URL(long_url=long_url)
        self.assertRaises(IntegrityError, url.save)

    def test_saves_same_url_with_different_hashes(self):
        long_url = "https://google.com"
        url_1 = create_url(long_url)
        url_2 = create_url(long_url)
        self.assertNotEqual(url_1.hashed_url, url_2.hashed_url)

    def test_rejects_invalid_url(self):
        long_url = "google"
        url = URL(long_url=long_url)
        self.assertRaises(ValidationError, url.save)


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


class GenerateHashTests(TestCase):
    def test_generates_string_of_settings_length(self):
        generated_hash = generate_hash()
        self.assertEqual(len(generated_hash), settings.HASH_LENGTH)

    def test_generated_string_uses_settings_characters(self):
        generated_hash = generate_hash()
        for character in generated_hash:
            self.assertIn(character, settings.HASH_CHARACTERS)
