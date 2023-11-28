import threading
import time
from screen_sync.stats import runtime_stats





class Coordinator:
    def __init__(self, bulbs, color_processing_module):
        self.bulbs = bulbs
        self.color_processing = color_processing_module
        self.lock = threading.Lock()
        self.mode = 'normal'
        self.running = False

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

    def capture_and_process_zone(self, bulb):
        while self.running:
            with self.lock:
                if self.mode == 'shooter':
                    color = self.color_processing.process_screen_zone('center')
                    bulb.set_color(*color)
                else:
                    color = self.color_processing.process_screen_zone(bulb.placement)
                    bulb.set_color(*color)
                runtime_stats.record_update()
            time.sleep(0.001)  # Add a small delay to avoid overloading

    def start(self):
        self.running = True
        self.threads = []
        for bulb in self.bulbs:
            t = threading.Thread(target=self.capture_and_process_zone, args=(bulb, ))
            t.start()
            self.threads.append(t)

    def stop(self):
        self.running = False
        for t in self.threads:
            t.join()

