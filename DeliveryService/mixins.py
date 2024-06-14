
from typing import Any

from django.core.cache import cache
from rest_framework.request import Request


class SessionManagementMixin:
    
    def ensure_session(self, request: Request):
        """
        Сreate session if there is none.

        Args:
            request: Request object.
        """

        if not request.session.session_key:
            request.session.create()

class CacheManagementMixin:

    def cache_or_select(self, response_data: Any, cache_key: str, timeout: int = 60 * 5) -> Any:
        """
        Return data from cache or from db.

        Args:
            response_data: value from Redis or from project db;
            cache_key: key in Redis db;
            timeout: lifespan for cache.
        """
        cached_response_data = cache.get(cache_key)
        if cached_response_data:
            return cached_response_data
        else:
            cache.set(key=cache_key, value=response_data, timeout=timeout)
        return response_data
