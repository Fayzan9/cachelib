from typing import (
    Callable,
    ParamSpec,
    Generic,
    TypeVar,
    Optional,
    Tuple,
    Dict,
    Hashable,
    Any,
)
from collections import OrderedDict
from threading import Lock
import time
import functools


K = TypeVar("K")
V = TypeVar("V")
P = ParamSpec("P")
R = TypeVar("R")


class LRUCache(Generic[K, V]):
    def __init__(self, max_size: int = 128, ttl: Optional[int] = None) -> None:
        self.max_size: int = max_size
        self.ttl: Optional[int] = ttl
        self.store: OrderedDict[K, Tuple[V, Optional[float]]] = OrderedDict()
        self.lock: Lock = Lock()

        self.hits: int = 0
        self.misses: int = 0
        self.evictions: int = 0

    def _is_expired(self, expiration_time: Optional[float]) -> bool:
        if expiration_time is None:
            return False
        return time.time() > expiration_time

    def _evict_if_needed(self) -> None:
        while len(self.store) > self.max_size:
            self.store.popitem(last=False)
            self.evictions += 1

    def set(self, key: K, value: V) -> None:
        with self.lock:
            expiration_time: Optional[float] = (
                time.time() + self.ttl if self.ttl is not None else None
            )

            if key in self.store:
                self.store.move_to_end(key)

            self.store[key] = (value, expiration_time)
            self._evict_if_needed()

    def get(self, key: K) -> Optional[V]:
        with self.lock:
            if key not in self.store:
                self.misses += 1
                return None

            value, expiration_time = self.store[key]

            if self._is_expired(expiration_time):
                del self.store[key]
                self.misses += 1
                return None

            self.store.move_to_end(key)
            self.hits += 1
            return value

    def stats(self) -> Dict[str, int]:
        with self.lock:
            return {
                "hits": self.hits,
                "misses": self.misses,
                "evictions": self.evictions,
                "current_size": len(self.store),
            }

    def delete(self, key: K) -> bool:
        with self.lock:
            if key in self.store:
                del self.store[key]
                return True
            return False

    def clear(self) -> None:
        with self.lock:
            self.store.clear()

    def __contains__(self, key: K) -> bool:
        with self.lock:
            if key not in self.store:
                return False

            _, expiration_time = self.store[key]

            if self._is_expired(expiration_time):
                del self.store[key]
                return False

            return True

    def resize(self, new_max_size: int) -> None:
        with self.lock:
            self.max_size = new_max_size
            self._evict_if_needed()


# ---------------- Decorator ----------------


def cache_decorator(
    ttl: Optional[int] = None,
    max_size: int = 128,
) -> Callable[[Callable[P, R]], Callable[P, R]]:

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache: LRUCache[
            Tuple[Hashable, Hashable], R
        ] = LRUCache(max_size=max_size, ttl=ttl)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = (make_hashable(args), make_hashable(kwargs))

            cached = cache.get(key)
            if cached is not None:
                return cached

            value = func(*args, **kwargs)
            cache.set(key, value)
            return value

        return wrapper

    return decorator


# ---------------- Hash Utility ----------------


def make_hashable(obj: Any) -> Hashable:
    if isinstance(obj, (tuple, list)):
        return tuple(make_hashable(item) for item in obj)

    if isinstance(obj, dict):
        return tuple(
            sorted(
                (make_hashable(k), make_hashable(v))
                for k, v in obj.items()
            )
        )

    if isinstance(obj, set):
        return frozenset(make_hashable(item) for item in obj)

    if isinstance(obj, Hashable):
        return obj

    raise TypeError(f"Unhashable type: {type(obj)}")