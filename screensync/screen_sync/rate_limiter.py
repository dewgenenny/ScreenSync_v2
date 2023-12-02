import time

class RateLimiter:
    def __init__(self, max_updates_per_second):
        self.min_interval = 1.0 / max_updates_per_second if max_updates_per_second else 0
        self.last_update_time = 0

    def is_allowed(self):
        """Check if an update is allowed based on the rate limit."""
        current_time = time.time()
        if current_time - self.last_update_time >= self.min_interval:
            self.last_update_time = current_time
            return True
        return False
