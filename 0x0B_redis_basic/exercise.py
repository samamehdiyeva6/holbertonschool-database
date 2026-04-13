#!/usr/bin/env python3
"""
This module defines a Cache class that interacts with a Redis database to store and retrieve data.
"""

import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper

class Cache:
    """
    A class with __init__ method and a private variable
    """
    def __init__(self) -> None:
        self._redis = redis.Redis(host='localhost', port=6379)
        self._redis.flushdb()


    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Metod that takes uuid data type and returns str
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
    
    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Metod that returns the value of key"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data
    
    def get_str(self, key: str) -> Optional[str]:
        """Metod that returns the value of key as str"""
        return self.get(key, lambda d: d.decode('utf-8'))
    
    def get_int(self, key: str) -> Optional[int]:
        """Metod that returns the value of key as int"""
        return self.get(key, lambda d: int(d.decode('utf-8')))


    def replay(method: Callable) -> None:
        """
        Replays the method and returns count of calls and history of calls
        """
        r = method.__self__._redis
        name = method.__qualname__
        count = r.get(name).decode('utf-8') if r.get(name) else '0'

        inputs = r.lrange(f"{name}:inputs", 0, -1)
        outputs = r.lrange(f"{name}:outputs", 0, -1)

        print(f"{name} was called {count} times:")

        for inp, out in zip(inputs, outputs):
            print(f"{name}(*{inp.decode('utf-8')})")