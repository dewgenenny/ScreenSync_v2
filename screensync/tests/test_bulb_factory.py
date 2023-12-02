import unittest
from unittest.mock import MagicMock, patch, ANY
from screen_sync.bulb_factory import BulbFactory
from screen_sync.config_manager import ConfigManager
class TestBulbFactory(unittest.TestCase):

    def setUp(self):
        # Mock ConfigManager with test configuration
        self.mock_config_manager = MagicMock(spec=ConfigManager)

        # Set up mock configurations
        self.mock_config_manager.get_mqtt_settings.return_value = {
            'broker': 'test_broker',
            'port': 1883,
            'username': 'test_user',
            'password': 'test_pass'
        }
        self.mock_config_manager.get_bulbs.return_value = [
            {'type': 'Tuya', 'device_id': 'id1', 'local_key': 'key1', 'ip_address': '192.0.2.1'},
            {'type': 'MQTT', 'topic': 'test/topic'}
        ]
        self.mock_config_manager.get_update_frequency.return_value = 10

        # Create an instance of BulbFactory with the mock ConfigManager
        self.bulb_factory = BulbFactory(self.mock_config_manager)

    @patch('screen_sync.bulb_factory.TuyaBulbControl')
    @patch('screen_sync.bulb_factory.ZigbeeBulbControl')
    def test_create_bulbs(self, mock_zigbee_bulb_control, mock_tuya_bulb_control):
        # Call create_bulbs and get the result
        bulbs = self.bulb_factory.create_bulbs()

        # Assert that the correct bulb objects were created
        mock_tuya_bulb_control.assert_called_once_with('id1', 'key1', '192.0.2.1', ANY)

        # Update the assertion to use named arguments for ZigbeeBulbControl
        mock_zigbee_bulb_control.assert_called_once_with(
            mqtt_broker='test_broker',
            port=1883,
            username='test_user',
            password='test_pass',
            topic='test/topic',
            rate_limiter=ANY
        )

        # Assert the correct number of bulbs were created
        self.assertEqual(len(bulbs), 2)

if __name__ == '__main__':
    unittest.main()
