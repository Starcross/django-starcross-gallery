from functools import wraps
from django.core.cache import cache

def cache_property(timeout=3600):
    """
    Caches a model method's result in the Django cache backend.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.pk:
                return func(self, *args, **kwargs)
            # Generate a unique key
            cache_key = f"{__package__}.{self.__class__.__name__}_{self.pk}_{func.__name__}"

            return cache.get_or_set(
                cache_key,
                lambda: func(self, *args, **kwargs),
                timeout=timeout
            )

        return property(wrapper)

    return decorator