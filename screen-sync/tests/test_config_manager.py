import unittest
from unittest.mock import patch, mock_open
from screen_sync.config_manager import ConfigManager
import configparser
import io

class MockFile:
    def __init__(self, initial_data):
        self.initial_data = initial_data
        self.reset()

    def reset(self):
        self.data = self.initial_data
        self.lines = iter(self.data.splitlines(keepends=True))

    def read(self):
        return self.data

    def write(self, new_data):
        self.data += new_data

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.lines)

    def __enter__(self):
        # For a mock, simply return self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # No action needed for the mock
        pass

    def readline(self):
        try:
            return next(self.lines)
        except StopIteration:
            return ''



class TestConfigManager(unittest.TestCase):

    def mock_file_open(self, file, mode='r', encoding=None):
        # Return the mock file object
        return self.mock_file

    def setUp(self):
        self.mock_file = MockFile(
            "[General]\n"
            "screen_capture_size=100, 100\n"
            "saturation_factor=1.5\n"
            "[BulbTuya1]\n"
            "device_id=123\n"
            "local_key=abc\n"
            "ip_address=192.168.1.2\n"
            "[BulbMQTT1]\n"
            "topic=zigbee2mqtt/xxx xxx/set\n"
        )
        self.patcher = patch('builtins.open', self.mock_file_open)
        self.patcher.start()
        self.mock_file.reset()

    # Add a method to get the updated configuration data for assertions
    def get_updated_config(self):
        config = configparser.ConfigParser()
        config.read_string(self.mock_file.data)
        return config

    def tearDown(self):
        # Stop patching 'open'
        self.patcher.stop()

    def test_load_config(self):
        config_manager = ConfigManager('./tests/test_config.ini')
        config_manager.load_config()


    def test_get_general_settings(self):
        config_manager = ConfigManager('./tests/test_config.ini')
        settings = config_manager.get_general_settings()
        self.assertEqual(settings['screen_capture_size'], (100, 100))
        self.assertEqual(settings['saturation_factor'], 1.5)

    def test_get_bulbs(self):
        config_manager = ConfigManager('./tests/test_config.ini')
        bulbs = config_manager.get_bulbs()
        # Find Tuya and MQTT bulbs in the returned list
        tuya_bulbs = [bulb for bulb in bulbs if bulb['type'] == 'Tuya']
        mqtt_bulbs = [bulb for bulb in bulbs if bulb['type'] == 'MQTT']

        # Check the presence and properties of Tuya bulbs
        self.assertGreaterEqual(len(tuya_bulbs), 1, "Should have at least one Tuya bulb")
        expected_tuya_properties = {'device_id', 'local_key', 'ip_address'}
        for prop in expected_tuya_properties:
            self.assertIn(prop, tuya_bulbs[0], f"Tuya bulb missing '{prop}' property")

        # Check the presence and properties of MQTT bulbs
        self.assertGreaterEqual(len(mqtt_bulbs), 1, "Should have at least one MQTT bulb")
        self.assertIn('topic', mqtt_bulbs[0], "MQTT bulb missing 'topic' property")

    def test_add_bulb(self):
        config_manager = ConfigManager('./tests/test_config.ini')
        config_manager.add_bulb('Tuya', device_id='new_device_id', local_key='new_local_key', ip_address='new_ip_address')
        self.mock_save_config(config_manager)  # Pass the config_manager instance
        updated_config = self.get_updated_config()
        self.assertIn('BulbTuya2', updated_config.sections())
        bulb_config = updated_config['BulbTuya2']
        self.assertEqual(bulb_config['device_id'], 'new_device_id')

    def mock_save_config(self, config_manager):
        config_string = io.StringIO()
        config_manager.config.write(config_string)
        self.mock_file.data = config_string.getvalue()

if __name__ == '__main__':
    unittest.main()
