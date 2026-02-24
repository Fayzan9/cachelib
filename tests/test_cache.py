
from cachelib import LRUCache, cache_decorator
import time
import threading
import pytest

def test_basic_set_get():
    cache = LRUCache(max_size=2)

    cache.set("a", 1)
    assert cache.get("a") == 1

    stats = cache.stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 0

def test_miss():
    cache = LRUCache(max_size=2)

    assert cache.get("missing") is None

    stats = cache.stats()
    assert stats["misses"] == 1

def test_lru_eviction():
    cache = LRUCache(max_size=2)

    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)  # should evict "a"

    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3

    stats = cache.stats()
    assert stats["evictions"] == 1

def test_ttl_expiration():
    cache = LRUCache(max_size=2, ttl=1)

    cache.set("x", 100)
    time.sleep(1.5)

    assert cache.get("x") is None

    stats = cache.stats()
    assert stats["misses"] == 1

def test_decorator_caching():
    call_count = 0

    @cache_decorator(max_size=10)
    def add(a, b):
        nonlocal call_count
        call_count += 1
        return a + b

    assert add(2, 3) == 5
    assert add(2, 3) == 5
    assert call_count == 1  # function should run once

def test_resize_shrinks_cache():
    cache = LRUCache(max_size=3)

    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)

    cache.resize(1)

    assert len(cache.store) == 1
    assert cache.stats()["evictions"] >= 2

def test_clear_does_not_reset_metrics():
    cache = LRUCache(max_size=2)

    cache.set("a", 1)
    cache.get("a")
    cache.clear()

    stats = cache.stats()
    assert stats["hits"] == 1

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (5, 6, 11),
        (-1, 1, 0),
    ],
)
def test_add_cases(a, b, expected):
    @cache_decorator(max_size=10)
    def add(x, y):
        return x + y

    assert add(a, b) == expected

def test_thread_safety():
    cache = LRUCache(max_size=5)

    def worker(i):
        for _ in range(1000):
            cache.set(i, i)
            cache.get(i)

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # If no crash and size <= max_size, test passes
    assert len(cache.store) <= 5