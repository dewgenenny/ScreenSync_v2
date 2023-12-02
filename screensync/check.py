import threading
import time
from collections import defaultdict
from screen_sync.stats import runtime_stats

class Coordinator:
    def __init__(self, bulbs, color_processing_module):
        self.bulbs = bulbs
        self.color_processing = color_processing_module
        self.mode = 'normal'
        self.running = False
        self.color_cache = defaultdict(lambda: (0, 0, 0))  # Default color is black
        self.lock = threading.Lock()

    def set_mode(self, mode):
        self.mode = mode
        # Any other updates required when changing modes

    def update_bulbs(self, new_bulbs):
        if self.running:
            self.stop()
        self.bulbs = new_bulbs
        self.start()
        if self.running:
            self.start()

    def update_bulb_color(self, bulb):
        while self.running:
            with self.lock:
                color = self.color_cache[bulb.placement]
                bulb.set_color(*color)
                runtime_stats.record_update()
            time.sleep(0.0001)  # Add a small delay to avoid overloading

    def start(self):
        self.running = True
        self.update_thread = threading.Thread(target=self.run_update_loop)
        self.update_thread.start()
        self.threads = [threading.Thread(target=self.update_bulb_color, args=(bulb,)) for bulb in self.bulbs]
        for thread in self.threads:
            thread.start()

    def run_update_loop(self):
        while self.running:
            # Update color cache based on current mode
            if self.mode == 'shooter':
                self.color_cache['center'] = self.color_processing.process_screen_zone('center', mode='Shooter')
            else:
                for bulb in self.bulbs:
                    self.color_cache[bulb.placement] = self.color_processing.process_screen_zone(bulb.placement)
            time.sleep(0.01)  # Adjust sampling rate as needed

    def stop(self):
        self.running = False
        if self.update_thread:
            self.update_thread.join()
        for t in self.threads:
            t.join()

# Usage in your main script
# coordinator = Coordinator(bulbs, color_processing)
# coordinator.start()  # This starts the processing and updating loop
