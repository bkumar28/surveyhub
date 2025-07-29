import hashlib
from functools import wraps

from django.conf import settings
from django.core.cache import cache


def cache_key_generator(*args, **kwargs):
    """Generate a cache key from function arguments"""
    key_data = str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(key_data.encode()).hexdigest()


def cached_function(timeout=None, key_prefix=""):
    """Decorator to cache function results"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = (
                f"{key_prefix}:{func.__name__}:{cache_key_generator(*args, **kwargs)}"
            )
            result = cache.get(cache_key)

            if result is None:
                result = func(*args, **kwargs)
                cache_timeout = timeout or getattr(
                    settings, "DEFAULT_CACHE_TIMEOUT", 300
                )
                cache.set(cache_key, result, cache_timeout)

            return result

        return wrapper

    return decorator


class CacheService:
    """Service class for common caching operations"""

    @staticmethod
    def get_survey_cache_key(survey_id):
        return f"survey:{survey_id}"

    @staticmethod
    def get_report_cache_key(survey_id):
        return f"survey_report:{survey_id}"

    @staticmethod
    def get_user_progress_key(user_token, survey_id):
        return f"user_progress:{user_token}:{survey_id}"

    @staticmethod
    def get_template_cache_key(template_id):
        return f"template:{template_id}"

    @staticmethod
    def cache_survey_data(survey):
        from surveys.serializers import SurveyDetailSerializer

        cache_key = CacheService.get_survey_cache_key(survey.id)
        serializer = SurveyDetailSerializer(survey)
        cache.set(cache_key, serializer.data, settings.SURVEY_CACHE_TIMEOUT)
        return serializer.data

    @staticmethod
    def get_cached_survey(survey_id):
        cache_key = CacheService.get_survey_cache_key(survey_id)
        return cache.get(cache_key)

    @staticmethod
    def invalidate_survey_cache(survey_id):
        cache_key = CacheService.get_survey_cache_key(survey_id)
        cache.delete(cache_key)
        # Also invalidate related report cache
        report_cache_key = CacheService.get_report_cache_key(survey_id)
        cache.delete(report_cache_key)

    @staticmethod
    def cache_report_data(survey_id, report_data):
        cache_key = CacheService.get_report_cache_key(survey_id)
        cache.set(cache_key, report_data, settings.REPORT_CACHE_TIMEOUT)

    @staticmethod
    def get_cached_report(survey_id):
        cache_key = CacheService.get_report_cache_key(survey_id)
        return cache.get(cache_key)

    @staticmethod
    def cache_user_progress(user_token, survey_id, progress_data):
        cache_key = CacheService.get_user_progress_key(user_token, survey_id)
        cache.set(cache_key, progress_data, settings.USER_SESSION_TIMEOUT)

    @staticmethod
    def get_user_progress(user_token, survey_id):
        cache_key = CacheService.get_user_progress_key(user_token, survey_id)
        return cache.get(cache_key)

    @staticmethod
    def clear_user_cache(user_token):
        """Clear all cache entries for a specific user"""
        # This would require a pattern-based cache clear
        # For now, we'll implement basic clearing
        pass
