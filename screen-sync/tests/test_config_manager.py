import unittest
from unittest.mock import patch, mock_open
from screen_sync.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        # Mocking the open function to prevent actual file I/O
        self.mock_open = mock_open()
        self.mock_open.return_value.__iter__ = lambda self: iter(["[General]\n", "screen_capture_size=100, 100\n", "saturation_factor=1.5\n", "[Bulb1]\n", "device_id=123\n", "local_key=abc\n", "ip_address=192.168.1.2\n"])
        self.patcher = patch('builtins.open', self.mock_open)
        self.patcher.start()

    def tearDown(self):
        # Stop patching 'open'
        self.patcher.stop()

    def test_load_config(self):
        config_manager = ConfigManager('config.ini')
        config_manager.load_config()
        self.mock_open.assert_called_with('config.ini', encoding='locale')
        self.assertIn('General', config_manager.config.sections())


    def test_get_general_settings(self):
        config_manager = ConfigManager('config.ini')
        settings = config_manager.get_general_settings()
        self.assertEqual(settings['screen_capture_size'], (100, 100))
        self.assertEqual(settings['saturation_factor'], 1.5)

    def test_get_bulbs(self):
        config_manager = ConfigManager('config.ini')
        bulbs = config_manager.get_bulbs()
        self.assertEqual(len(bulbs), 1)
        self.assertEqual(bulbs[0]['device_id'], '123')

    def test_add_bulb(self):
        config_manager = ConfigManager('config.ini')
        config_manager.add_bulb('new_device_id', 'new_local_key', 'new_ip_address')
        self.assertIn('Bulb2', config_manager.config.sections())
        bulb_config = config_manager.config['Bulb2']
        self.assertEqual(bulb_config['device_id'], 'new_device_id')

if __name__ == '__main__':
    unittest.main()
