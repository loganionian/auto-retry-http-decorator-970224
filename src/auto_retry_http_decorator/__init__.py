"""
auto_retry_http_decorator package.

This package provides a decorator for automatically retrying HTTP requests
with exponential backoff and a circuit breaker pattern.
"""

from .core import retry

__all__ = ["retry"]