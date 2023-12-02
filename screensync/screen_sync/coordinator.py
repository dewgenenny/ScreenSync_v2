import threading
import time
from collections import defaultdict
from screensync.screen_sync.stats import runtime_stats

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

    def update_bulb_color(self, bulb, color):
        # Update the bulb color in a new thread
        t = threading.Thread(target=bulb.set_color, args=color)
        t.start()
        self.threads.append(t)

    def start(self):
        self.running = True
        self.update_thread = threading.Thread(target=self.run_update_loop)
        self.update_thread.start()
        self.threads = [threading.Thread(target=self.update_bulb_color, args=(bulb,)) for bulb in self.bulbs]
        for thread in self.threads:
            thread.start()


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
        for t in self.threads:
            t.join()

# Usage in your main script
# coordinator = Coordinator(bulbs, color_processing)
# coordinator.start()  # This starts the processing and updating loop
