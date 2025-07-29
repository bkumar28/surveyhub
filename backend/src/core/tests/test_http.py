import unittest

from core.http_ import Http404, HttpError
from rest_framework import status


class TestHttpExceptions(unittest.TestCase):
    def test_http404_default(self):
        exc = Http404()
        self.assertEqual(exc.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Failed", exc.detail["status"])

    def test_http404_custom(self):
        exc = Http404(message="Not found", error_code=123)
        self.assertEqual(exc.detail["message"], "Not found")
        self.assertEqual(exc.detail["code"], 123)

    def test_http_error_default(self):
        exc = HttpError()
        self.assertEqual(exc.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Failed", exc.detail["status"])

    def test_http_error_custom(self):
        exc = HttpError(message="Bad req", error_code=456)
        self.assertEqual(exc.detail["message"], "Bad req")
        self.assertEqual(exc.detail["code"], 456)
