import configparser
import os


class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def get_config_by_section(self, section):
        return dict(self.config.items(section))

    def create_default_config(self):
        """Creates a default configuration file."""
        # Add default sections and settings
        self.config['General'] = {
            'screen_capture_size': '100, 100',
            'saturation_factor': '1.5'
        }
        self.config['MQTT'] = {
            'broker': 'localhost',
            'port': '1883',
            'username': '',
            'password': ''
        }

        # Add default TuyaSettings
        self.config['TuyaSettings'] = {
            'update_frequency': '50'
        }

        # Add default MQTTSettings
        self.config['MQTTSettings'] = {
            'update_frequency': '0.5'
        }

        # Add default MagicHomeSettings
        self.config['MagicHomeSettings'] = {
            'update_frequency': '50'
        }

        # Add more default sections and settings as necessary

        # Create the config file with default settings
        with open(self.config_file, 'w') as file:
            self.config.write(file)


    def load_config(self):
        """Loads the configuration file, creates one if it doesn't exist."""
        if not os.path.exists(self.config_file):
            self.create_default_config()
        else:
            self.config.read(self.config_file)

    def save_config(self):
        """Saves the configuration to the file."""
        with open(self.config_file, 'w') as file:
            self.config.write(file)

    def get_general_settings(self):
        """Retrieves general settings from the config."""
        general = self.config['General']
        return {
            'screen_capture_size': tuple(map(int, general.get('screen_capture_size', '100, 100').split(','))),
            'saturation_factor': general.getfloat('saturation_factor', 1.5)
        }

    def get_section_by_device_id(self, device_id):
        for section in self.config.sections():
            if self.config[section].get('device_id') == device_id:
                return section
        return None  # Or raise an error

    def get_bulbs(self):
        """Retrieves bulb configurations for different types."""
        bulbs = []
        for section in self.config.sections():
            if section.startswith('BulbTuya'):
                bulbs.append({
                    'type': 'Tuya',
                    'device_id': self.config[section]['device_id'],
                    'local_key': self.config[section]['local_key'],
                    'ip_address': self.config[section]['ip_address'],
                    'placement': self.config[section].get('placement', 'center'),  # Default placement is 'Center'
                    'config_id' : section
                })
            elif section.startswith('BulbMagicHome'):
                bulbs.append({
                    'type': 'MagicHome',
                    'ip_address': self.config[section]['ip_address'],
                    'device_id': 'MagicHome',
                    'placement': self.config[section].get('placement', 'center'),  # Default placement is 'Center'
                    'config_id' : section
                })

            elif section.startswith('BulbMQTT'):
                bulbs.append({
                    'type': 'MQTT',
                    'topic': self.config[section]['topic'],
                    'placement': self.config[section].get('placement', 'center'),  # Default placement is 'Center'
                    'device_id': 'MQTT',
                    'config_id' : section
                })
            # Add more elif blocks for other bulb types as needed

        return bulbs

    def get_mqtt_settings(self):
        """Retrieves MQTT settings from the config."""
        mqtt = self.config['MQTT']
        return {
            'broker': mqtt.get('broker', 'localhost'),
            'port': mqtt.getint('port', 1883),
            'username': mqtt.get('username', ''),
            'password': mqtt.get('password', '')
        }

    def set_mqtt_settings(self, broker, port, username, password):
        """Sets MQTT settings."""
        if 'MQTT' not in self.config.sections():
            self.config.add_section('MQTT')
        self.config['MQTT'] = {
            'broker': broker,
            'port': str(port),
            'username': username,
            'password': password
        }
        self.save_config()


    def add_bulb(self, bulb_type, **kwargs):
        """Adds a new bulb configuration based on the bulb type."""
        if bulb_type == 'MQTT':
            self._add_mqtt_bulb(**kwargs)
        elif bulb_type == 'Tuya':
            self._add_tuya_bulb(**kwargs)
        # Add more elif blocks for other bulb types as needed

    def _add_mqtt_bulb(self, topic, placement):
        """Adds a new MQTT bulb configuration."""
        mqtt_bulb_count = len([s for s in self.config.sections() if s.startswith('BulbMQTT')])
        section_name = f'BulbMQTT{mqtt_bulb_count + 1}'
        self.config[section_name] = {

            'topic': topic,
            'placement': placement

        }
        self.save_config()

    def _add_tuya_bulb(self, device_id, local_key, ip_address, placement):
        """Adds a new Tuya bulb configuration."""
        tuya_bulb_count = len([s for s in self.config.sections() if s.startswith('BulbTuya')])
        section_name = f'BulbTuya{tuya_bulb_count + 1}'

        self.config[section_name] = {
            'device_id': device_id,
            'local_key': local_key,
            'ip_address': ip_address,
            'placement': placement
        }
        self.save_config()


    def get_update_frequency(self, bulb_type):
        """Retrieves the update frequency for a given bulb type."""
        section = f'{bulb_type}Settings'
        return self.config.getfloat(section, 'update_frequency', fallback=10)  # Default to 10 updates per second

    def set_update_frequency(self, bulb_type, frequency):
        """Sets the update frequency for a given bulb type."""
        section = f'{bulb_type}Settings'
        if section not in self.config.sections():
            self.config.add_section(section)
        self.config[section]['update_frequency'] = str(frequency)
        self.save_config()


# Example Usage
if __name__ == "__main__":
    config_manager = ConfigManager("..\config.ini")
    # Add a new bulb
    # config_manager.add_bulb('new_device_id', 'new_local_key', 'new_ip_address')
