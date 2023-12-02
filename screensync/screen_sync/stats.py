import time
import functools
from collections import deque

class RuntimeStats:
    def __init__(self):
        self.stats = {}
        self.history = deque(maxlen=300)  # Holds 5 minutes of data, assuming 1 data point per second
        self.last_update_time = None
        self.updates_this_second = 0

    def get_last_n_stats(self, n):
        """Get the last n updates per second data points."""
        # Return the last n elements from the history deque
        # If n is greater than the length of history, return the entire history
        return list(self.history)[-n:]

    def record_update(self):
        current_time = time.time()
        if self.last_update_time and current_time - self.last_update_time < 1:
            self.updates_this_second += 1
        else:
            self.history.append((current_time, self.updates_this_second))
            self.updates_this_second = 1
            self.last_update_time = current_time

    def timed_function(self, stat_key):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                self.stats[stat_key] = elapsed_time
                return result
            return wrapper
        return decorator

    def display_stats(self):
        print("---- Runtime Statistics ----")
        for key, value in self.stats.items():
            print(f"{key}: {value:.2f} seconds")
        current_updates_per_second = self.updates_this_second
        print(f"Current Updates/Sec: {current_updates_per_second}")
        for timestamp, updates in list(self.history)[-10:]:  # Show last 10 data points
            time_str = time.strftime("%H:%M:%S", time.localtime(timestamp))
            print(f"{time_str}: {updates} updates/sec")
        print("----------------------------")

# Global instance to be used across the application
runtime_stats = RuntimeStats()
