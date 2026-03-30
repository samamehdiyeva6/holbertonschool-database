#!/usr/bin/env python3
"""
This module has a Cache class with __init__ method and a private variable 
"""
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Uses functional wrapper to count calls
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wraps the function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Uses functional wrapper to call history
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wraps the function
        """
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(inputs_key, str(args))
        result =  method(self, *args, **kwargs)
        self._redis.lpush(outputs_key, result)
        return result
    return wrapper

class Cache:
    """
    A class with __init__ method and a private variable
    """
    def __init__(self) -> None:
        """
        Method that initializes redis instance and flushes the db
        """
        import redis
        
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Metod that takes uuid data type and returns str
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
    
    def get(self, key: str, fn: Optional[Callable] = None) -> Union[int, bytes, float, str, None]:
        """
        Retrieves data from redis and applies optional conversion
        """
        data = self._redis.get(key)
        if key is not None and fn is not None:
            return fn(data) 
        return data

    def get_str(self, key: str) -> str:
        """
        Converts redis bytes into string
        """
        key = self.get(key, lambda d: d.decode("utf-8"))
        return key

    def get_int(self, key: int) -> int:
        """
        Converts redis bytes into integer
        """
        key = self.get(key, int)
        return key

    def replay(method: Callable) -> None:
        """
        Replays the method and returns count of calls and history of calls
        """
        r = method.__self__._redis
        name = method.__qualname__
        count = r.get(name)
        count_int = int(count.decode("utf-8")) if count else 0

        inputs = r.lrange(f"{name}:inputs", 0, -1)
        outputs = r.lrange(f"{name}:outputs" 0, -1)

        for inp, out in zip(inputs, outputs):
            print(f"{name}(*{inp.decode("utf-8")} -> {out.decode("utf-8")})")
    
    