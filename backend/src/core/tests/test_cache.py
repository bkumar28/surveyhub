import unittest
from unittest.mock import patch

from core import cache


class TestCacheKeyGenerator(unittest.TestCase):
    def test_cache_key_generator(self):
        key1 = cache.cache_key_generator(1, 2, a=3)
        key2 = cache.cache_key_generator(1, 2, a=3)
        self.assertEqual(key1, key2)
        key3 = cache.cache_key_generator(2, 1, a=3)
        self.assertNotEqual(key1, key3)


class TestCachedFunction(unittest.TestCase):
    @patch("core.cache.cache")
    def test_cached_function_decorator(self, mock_cache):
        mock_cache.get.return_value = None

        @cache.cached_function(timeout=1, key_prefix="test")
        def add(a, b):
            return a + b

        result = add(1, 2)
        self.assertEqual(result, 3)
        self.assertTrue(mock_cache.set.called)


class TestCacheService(unittest.TestCase):
    def test_get_survey_cache_key(self):
        self.assertEqual(cache.CacheService.get_survey_cache_key(1), "survey:1")

    def test_get_report_cache_key(self):
        self.assertEqual(cache.CacheService.get_report_cache_key(2), "survey_report:2")

    def test_get_user_progress_key(self):
        self.assertEqual(
            cache.CacheService.get_user_progress_key("token", 3),
            "user_progress:token:3",
        )

    def test_get_template_cache_key(self):
        self.assertEqual(cache.CacheService.get_template_cache_key(4), "template:4")
