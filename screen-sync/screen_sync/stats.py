import time
import functools

class RuntimeStats:
    def __init__(self):
        self.stats = {}

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
        print("----------------------------")

# Global instance to be used across the application
runtime_stats = RuntimeStats()
