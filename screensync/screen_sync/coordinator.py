import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from screensync.screen_sync.stats import runtime_stats

class Coordinator:
    def __init__(self, bulbs, color_processing_module):
        self.bulbs = bulbs
        self.color_processing = color_processing_module
        self.mode = 'normal'
        self.running = False
        self.color_cache = defaultdict(lambda: (0, 0, 0))  # Default color is black
        self.lock = threading.Lock()
        self.executor = None
        self.update_thread = None
        self._create_executor()

    def set_mode(self, mode):
        self.mode = mode
        # Any other updates required when changing modes

    def update_bulbs(self, new_bulbs):
        if self.running:
            self.stop()
        self.bulbs = new_bulbs
        self._reset_executor()
        self.start()

    def update_bulb_color(self, bulb, color):
        args = color if isinstance(color, (tuple, list)) else (color,)

        if not self.executor:
            bulb.set_color(*args)
            return

        try:
            self.executor.submit(bulb.set_color, *args)
        except RuntimeError:
            # Executor has been shut down; fall back to synchronous update
            bulb.set_color(*args)

    def start(self):
        if self.running:
            return

        if not self.executor:
            self._create_executor()

        self.running = True
        self.update_thread = threading.Thread(target=self.run_update_loop)
        self.update_thread.start()


    def run_update_loop(self):
        while self.running:
            # Record update for stats
            runtime_stats.record_update()

            if self.mode == 'shooter':
                # In shooter mode, capture the screen once for the center
                center_color = self.color_processing.process_screen_zone('center', mode='Shooter')
                for bulb in self.bulbs:
                    # Update all bulbs with the center color
                    self.update_bulb_color(bulb, center_color)
            else:
                # In normal mode, update each bulb based on its zone
                for bulb in self.bulbs:
                    zone_color = self.color_processing.process_screen_zone(bulb.placement)
                    self.update_bulb_color(bulb, zone_color)

            # Sleep to avoid overloading
            time.sleep(0.0001)


    def stop(self):
        self.running = False
        if self.update_thread:
            self.update_thread.join()
            self.update_thread = None

        if self.executor:
            self.executor.shutdown(wait=True)
            self.executor = None

    def _create_executor(self):
        if self.executor is None:
            max_workers = max(1, len(self.bulbs)) if self.bulbs else 1
            self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def _reset_executor(self):
        if self.executor:
            self.executor.shutdown(wait=True)
            self.executor = None
        self._create_executor()

# Usage in your main script
# coordinator = Coordinator(bulbs, color_processing)
# coordinator.start()  # This starts the processing and updating loop
