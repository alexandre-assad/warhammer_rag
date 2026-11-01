import threading
import time

from google.api_core.exceptions import ResourceExhausted


class RateLimiter:

    def __init__(self, requests_per_minute: int):
        self._interval = 60.0 / requests_per_minute
        self._lock = threading.Lock()
        self._next_slot = 0.0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            slot = max(now, self._next_slot)
            self._next_slot = slot + self._interval
        if slot - now > 0.05:
            time.sleep(slot - now)


limiter = RateLimiter(4)  

def call_with_retry(fn, *args, retries: int = 5, **kwargs):
    for attempt in range(retries):
        limiter.wait()
        try:
            return fn(*args, **kwargs)
        except ResourceExhausted:
            if attempt == retries - 1:
                raise
            time.sleep(40 * (attempt + 1))