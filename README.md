# cachelib

![CI](https://github.com/Fayzan9/cachelib/actions/workflows/ci.yml/badge.svg)

Thread-safe LRU cache with TTL and decorator support, built with strict typing, high test coverage, and modern Python packaging practices.

---

## Overview

`cachelib` provides a production-ready in-memory LRU (Least Recently Used) cache with:

- Thread safety
- Optional TTL (time-to-live) expiration
- Decorator-based caching
- Strict type hints (mypy --strict clean)
- High test coverage
- Modern `src/` layout packaging

This project was built to demonstrate professional Python engineering practices including testing, linting, CI, and semantic versioning.

---

## Features

- ✅ LRU eviction policy
- ✅ Optional TTL expiration
- ✅ Thread-safe operations
- ✅ Function decorator interface
- ✅ Robust argument normalization (handles nested structures)
- ✅ Strict static typing
- ✅ 90%+ test coverage
- ✅ GitHub Actions CI

---

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/<your-username>/cachelib.git
cd cachelib
pip install -e .
Quick Start
Using the Cache Class
from cachelib import LRUCache

cache = LRUCache[str, int](max_size=2, ttl=10)

cache.set("a", 1)
print(cache.get("a"))  # 1
print(cache.stats())
Using the Decorator
from cachelib import cache_decorator
import time

@cache_decorator(ttl=5, max_size=100)
def slow_add(a: int, b: int) -> int:
    time.sleep(1)
    return a + b

print(slow_add(2, 3))  # Slow first call
print(slow_add(2, 3))  # Fast (cached)

print(slow_add.cache.stats())
TTL Behavior

If TTL is provided:

Entries expire after ttl seconds

Expired entries are treated as cache misses

Expired entries are removed lazily on access

Example:

cache = LRUCache[str, int](max_size=2, ttl=1)

cache.set("x", 100)
time.sleep(1.5)

print(cache.get("x"))  # None (expired)
Metrics

The cache tracks:

hits

misses

evictions

size

Access metrics:

print(cache.stats())
Thread Safety

All public methods are protected by a lock.

The cache is safe for concurrent reads and writes across multiple threads.

Note:
Duplicate computation may occur if multiple threads request the same uncached key simultaneously (no single-flight deduplication).

Project Structure
cachelib/
├── pyproject.toml
├── src/
│   └── cachelib/
│       ├── __init__.py
│       └── lrucache.py
├── tests/
│   └── test_cache.py
└── .github/workflows/
    └── ci.yml
Development

Install development dependencies:

pip install pytest pytest-cov mypy ruff black

Run tests:

pytest --cov=.

Run type checking:

mypy src --strict

Run linting:

ruff check .

Format code:

black .
Versioning

This project follows Semantic Versioning:

MAJOR version for incompatible API changes

MINOR version for backward-compatible features

PATCH version for backward-compatible bug fixes

Example:

0.1.0
Future Improvements

Async support

Single-flight deduplication

Pluggable backends (Redis, Memcached)

Performance benchmarking suite

Prometheus metrics integration

License

MIT License

Author

Faizan
Software Developer focused on production-grade Python engineering and AI systems.


---

# What This README Does Well

- Clear purpose
- Concrete examples
- Professional structure
- Development instructions
- Honest limitations
- Future roadmap
- Engineering signals

---

Once you:

1. Replace `<your-username>`
2. Commit
3. Push

Tell me:

- Did the CI badge turn green?
- Do you want to improve it further (add usage GIF, benchmarks, or PyPI publishing)?

Next we move into building your AI production service template.