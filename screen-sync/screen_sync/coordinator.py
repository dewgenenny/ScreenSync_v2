import threading
import time


class Coordinator:
    def __init__(self, bulbs, color_processing_module):
        self.bulbs = bulbs
        self.color_processing = color_processing_module
        self.lock = threading.Lock()
        self.running = False


    def capture_and_process_zone(self, bulb):
        while self.running:
            with self.lock:
                color = self.color_processing.process_screen_zone(bulb.placement)
                bulb.set_color(*color)
            time.sleep(0.01)  # Add a small delay to avoid overloading

    def start(self):
        self.running = True
        self.threads = []
        for bulb in self.bulbs:
            t = threading.Thread(target=self.capture_and_process_zone, args=(bulb,))
            t.start()
            self.threads.append(t)

    def stop(self):
        self.running = False
        for t in self.threads:
            t.join()

