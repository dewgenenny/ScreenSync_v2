import tinytuya
from .abstract_bulb_control import AbstractBulbControl

def generate_dp27_string(self, hue, saturation, value, mode='gradient'):
    """Generate the DP27 string manually with given hue, saturation, and value."""
    h_hex = '{:04x}'.format(hue)
    s_hex = '{:04x}'.format(saturation)
    v_hex = '{:04x}'.format(value)

    mode_flag = '1' if mode == 'gradient' else '0'
    dp27_string = f"0{h_hex}{s_hex}{v_hex}00000000"  # Additional brightness/color temp set to max
    return dp27_string

class TuyaBulbControl(AbstractBulbControl):

    def __init__(self, device_id, local_key, ip):
        self.device_id = device_id
        self.local_key = local_key
        self.ip = ip
        self.bulb = None

    def connect(self):
        self.bulb = tinytuya.BulbDevice(self.device_id, self.ip, self.local_key, persist=True)
        self.bulb.set_version(3.3)
        self.bulb.set_socketRetryLimit(1)
        self.bulb.set_socketTimeout(1)
        self.bulb.set_retry(retry=False)
        self.bulb.set_socketPersistent(True)


    def set_color(self, h,s,v):
        dp27_string = generate_dp27_string(self,h,s,v)
        if self.bulb:
            self.bulb.set_multiple_values( {'21': 'music', '27': dp27_string}, nowait=True)

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
