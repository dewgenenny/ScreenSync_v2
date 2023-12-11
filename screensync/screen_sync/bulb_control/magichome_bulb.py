from flux_led import WifiLedBulb
from ..rate_limiter import RateLimiter
from .abstract_bulb_control import AbstractBulbControl

class FluxLedBulbControl:

#FluxLedBulbControl(bulb_config['ip_address'], color_mode, placement, rate_limiter)

    def __init__(self, ip_address, color_mode, placement, rate_limiter):
        self.bulb = WifiLedBulb(ip_address, timeout=1)
        self.rate_limiter = rate_limiter
        self.last_color = None
        self.placement = placement
        self.type = "MagicHome"
        self.ip = ip_address
        self.color_mode = color_mode


    def set_color(self, r, g, b):

        new_color = (r, g, b)

        if new_color == self.last_color:
            return  # No change in color, no need to update


        if self.rate_limiter.is_allowed():

            if self.bulb:
                if self.color_mode == "rgb":
                    self.bulb.setRgb(r, g, b)
                elif self.color_mode == "rbg":
                    self.bulb.setRgb(r, b, g)
                elif self.color_mode == "grb":
                    self.bulb.setRgb(g, r, b)
                elif self.color_mode == "gbr":
                    self.bulb.setRgb(g, b, r)
                elif self.color_mode == "brg":
                    self.bulb.setRgb(b, r, g)
                elif self.color_mode == "bgr":
                    self.bulb.setRgb(b, g, r)

            self.last_color = new_color  # Store the new color

    def connect(self):
        try:
            self.bulb.connect(retry=1)
        except:
            print("Bulb " + self.type + " - " + self.ip + "Unavailable")
