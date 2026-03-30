#!/usr/bin/env python3
"""
This module defines a Cache class that interacts with a Redis database to store and retrieve data.
"""

import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps

def count_calls(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        key = f.__qualname__
        self._redis.incr(key)
        return f(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis(host='localhost', port=6379)
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data
    
    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, lambda d: d.decode('utf-8'))
    
    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, lambda d: int(d.decode('utf-8')))
