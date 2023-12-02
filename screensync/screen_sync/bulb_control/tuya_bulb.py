import tinytuya
from .abstract_bulb_control import AbstractBulbControl
from ..rate_limiter import RateLimiter
import colorsys
import time
from screensync.screen_sync.stats import runtime_stats

def generate_dp27_string(self, hue, saturation, value, mode='gradient'):
    """Generate the DP27 string manually with given hue, saturation, and value."""
    h_hex = '{:04x}'.format(hue)
    s_hex = '{:04x}'.format(saturation)
    v_hex = '{:04x}'.format(value)

    mode_flag = '1' if mode == 'gradient' else '0'
    dp27_string = f"0{h_hex}{s_hex}{v_hex}00000000"  # Additional brightness/color temp set to max
    return dp27_string

class TuyaBulbControl(AbstractBulbControl):

    def __init__(self, device_id, local_key, ip, rate_limiter, placement):
        self.device_id = device_id
        self.local_key = local_key
        self.ip = ip
        self.bulb = None
        self.rate_limiter = rate_limiter
        self.last_color = None
        self.placement = placement
        self.type = "Tuya"


    def connect(self):
        self.bulb = tinytuya.BulbDevice(self.device_id, self.ip, self.local_key, persist=True)
        self.bulb.set_version(3.3)
        self.bulb.set_socketRetryLimit(1)
        self.bulb.set_socketTimeout(1)
        self.bulb.set_retry(retry=False)
        self.bulb.set_socketPersistent(True)

    @runtime_stats.timed_function('update_tuya_bulb')
    def set_color(self, r,g,b):
        """We are using the music-sync DPS (27) to update the bulb. It seems to be more performant."""

        """Converts RGB to HSV and sets the color of the Tuya bulb."""
        # Convert RGB to HSV

        new_color = (r, g, b)
        if new_color == self.last_color:
            return  # No change in color, no need to update


        if self.rate_limiter.is_allowed():
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

            # Scale HSV values to the appropriate range
            h_scaled = int(h * 360)  # Hue: 0-360
            s_scaled = int(s * 1000) # Saturation: 0-1000
            v_scaled = int(v * 1000) # Value: 0-1000

            dp27_string = generate_dp27_string(self,h_scaled,s_scaled,v_scaled)
            if self.bulb:
                self.bulb.set_multiple_values( {'21': 'music', '27': dp27_string}, nowait=True)
            self.last_color = new_color  # Store the new color


    def turn_off(self):
        if self.bulb:
            self.bulb.turn_off()

    def turn_on(self):
        if self.bulb:
            self.bulb.set_mode(mode='white',nowait=True)
            self.bulb.turn_on()

    def status(self):
        if self.bulb:
            return self.bulb.status()
