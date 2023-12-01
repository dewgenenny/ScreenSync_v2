from flux_led import WifiLedBulb
from ..rate_limiter import RateLimiter
from .abstract_bulb_control import AbstractBulbControl

class FluxLedBulbControl:

    def __init__(self, ip_address, placement, rate_limiter):
        self.bulb = WifiLedBulb(ip_address)
        self.rate_limiter = rate_limiter
        self.last_color = None
        self.placement = placement
        self.type = "MagicHome"
        self.ip = ip_address


    def set_color(self, r, g, b):

        new_color = (r, g, b)
        if new_color == self.last_color:
            return  # No change in color, no need to update


        if self.rate_limiter.is_allowed():


            if self.bulb:
                self.bulb.setRgb(r, g, b)
            self.last_color = new_color  # Store the new color

    def connect(self):
        self.bulb.connect()
