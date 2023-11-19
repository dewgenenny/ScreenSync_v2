import tinytuya
from .abstract_bulb_control import AbstractBulbControl

class TuyaBulbControl(AbstractBulbControl):
    def __init__(self, device_id, local_key, ip):
        self.device_id = device_id
        self.local_key = local_key
        self.ip = ip
        self.bulb = None

    def connect(self):
        self.bulb = tinytuya.BulbDevice(self.device_id, self.ip, self.local_key, persist=True)
        self.bulb.set_version(3.3)

    def set_color(self, r, g, b):
        if self.bulb:
            self.bulb.set_colour(r, g, b)

    def turn_off(self):
        if self.bulb:
            self.bulb.turn_off()

    def turn_on(self):
        if self.bulb:
            self.bulb.turn_on()
