import configparser

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Loads the configuration file."""
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

    def get_bulbs(self):
        """Retrieves bulb configurations."""
        bulbs = []
        for section in self.config.sections():
            if section.startswith('Bulb'):
                bulbs.append({
                    'device_id': self.config[section]['device_id'],
                    'local_key': self.config[section]['local_key'],
                    'ip_address': self.config[section]['ip_address']
                })
        return bulbs

    def add_bulb(self, device_id, local_key, ip_address):
        """Adds a new bulb configuration."""
        section_name = f'Bulb{len(self.config.sections())}'
        self.config[section_name] = {
            'device_id': device_id,
            'local_key': local_key,
            'ip_address': ip_address
        }
        self.save_config()

# Example Usage
if __name__ == "__main__":
    config_manager = ConfigManager("..\config.ini")
    print(config_manager.get_general_settings())
    print(config_manager.get_bulbs())
    # Add a new bulb
    # config_manager.add_bulb('new_device_id', 'new_local_key', 'new_ip_address')
