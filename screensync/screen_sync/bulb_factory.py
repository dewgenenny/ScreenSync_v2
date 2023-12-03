from screensync.screen_sync.bulb_control.tuya_bulb import TuyaBulbControl
from screensync.screen_sync.bulb_control.zigbee_bulb import ZigbeeBulbControl
from screensync.screen_sync.bulb_control.magichome_bulb import FluxLedBulbControl
from screensync.screen_sync.rate_limiter import RateLimiter
# Import other bulb control classes as needed

class BulbFactory:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def create_bulbs(self):
        """Creates and returns bulb objects based on the configuration."""
        bulbs = []
        mqtt_settings = self.config_manager.get_mqtt_settings()

        for bulb_config in self.config_manager.get_bulbs():
            bulb_type = bulb_config.get('type')
            frequency = self.config_manager.get_update_frequency(bulb_type)
            rate_limiter = RateLimiter(frequency)  # Instantiate RateLimiter
            placement = bulb_config.get('placement', 'center')
            if bulb_config['type'] == 'MagicHome':
                try:
                    bulb = FluxLedBulbControl(bulb_config['ip_address'], placement, rate_limiter)
                    bulbs.append(bulb)
                except:
                    print("Error adding " + bulb.type + "  bulb with IP " + bulb_config['ip_address'] )
            elif bulb_type == 'Tuya':
                try:
                    bulb = TuyaBulbControl(bulb_config['device_id'], bulb_config['local_key'], bulb_config['ip_address'], rate_limiter, placement)
                    bulbs.append(bulb)
                except:
                    print("Error adding " + bulb.type + "  bulb with IP " + bulb_config['ip_address'] )
            elif bulb_type == 'MQTT':
                try:
                    bulb = ZigbeeBulbControl(
                        mqtt_broker=mqtt_settings['broker'],
                        port=mqtt_settings['port'],
                        username=mqtt_settings['username'],
                        password=mqtt_settings['password'],
                        topic=bulb_config['topic'],
                        rate_limiter=rate_limiter,
                        placement=placement
                    )
                    bulb.turn_on()
                    bulb.connect()
                    bulbs.append(bulb)
                except:
                    print("Error adding " + bulb.type + "  bulb with MQTT broker " + mqtt_broker )
                pass
            # Add more conditions for other bulb types

            if bulb:

                bulb.connect()

        return bulbs
