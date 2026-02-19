import time
import logging
import functools
from requests import RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CircuitBreaker:
    """A simple circuit breaker implementation."""
    def __init__(self, failure_threshold=3, recovery_timeout=5):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.is_open():
            logger.warning("Circuit breaker is open. Skipping call.")
            return None
        try:
            result = func(*args, **kwargs)
            self.reset()
            return result
        except RequestException as e:
            self.record_failure()
            logger.error(f"Request failed: {e}")
            raise

    def is_open(self):
        if self.failure_count >= self.failure_threshold:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.reset()
                return False
            return True
        return False

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

    def reset(self):
        self.failure_count = 0
        self.last_failure_time = None


def retry(max_attempts=3, delay=1):
    """
    A decorator for retrying failed HTTP requests.

    Args:
        max_attempts (int): Maximum number of retry attempts.
        delay (int): Initial delay in seconds before retrying.

    Returns:
        Callable: A wrapped function that will retry on failure.
    """
    def decorator(func):
        circuit_breaker = CircuitBreaker()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return circuit_breaker.call(func, *args, **kwargs)
                except RequestException:
                    attempts += 1
                    logger.info(f"Retrying... Attempt {attempts + 1}")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
            logger.error("Max attempts reached. Raising exception.")
            raise

        return wrapper

    return decorator