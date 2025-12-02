# src/cache.py
from diskcache import Cache
from pathlib import Path


_cache = Cache(directory=Path.cwd() / "cache")


def cached(key, expire_seconds=None):
def decorator(func):
def wrapper(*args, **kwargs):
force = kwargs.pop("force_refresh", False)
cache_key = (func.__name__, args, frozenset(kwargs.items()))
if not force and cache_key in _cache:
return _cache[cache_key]
result = func(*args, **kwargs)
_cache.set(cache_key, result, expire=expire_seconds)
return result
return wrapper
return decorator
