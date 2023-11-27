import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from screen_sync.bulb_control.tuya_bulb import TuyaBulbControl, generate_dp27_string

class TestTuyaBulbControl(unittest.TestCase):

    @patch('screen_sync.bulb_control.tuya_bulb.tinytuya.BulbDevice')
    def test_connect(self, mock_bulb_device):
        # Setup
        bulb_control = TuyaBulbControl('device_id', 'local_key', 'ip')
        mock_bulb = MagicMock()
        mock_bulb_device.return_value = mock_bulb

        # Test
        bulb_control.connect()
        mock_bulb_device.assert_called_with('device_id', 'ip', 'local_key', persist=True)
        mock_bulb.set_version.assert_called_with(3.3)
        self.assertIsNotNone(bulb_control.bulb)

    @patch('screen_sync.bulb_control.tuya_bulb.tinytuya.BulbDevice')
    def test_set_color(self, mock_bulb_device):
        # Setup
        bulb_control = TuyaBulbControl('device_id', 'local_key', 'ip')
        mock_bulb = MagicMock()
        bulb_control.bulb = mock_bulb

        # Test
        bulb_control.set_color(120, 1000, 1000)
        expected_dp27_string = generate_dp27_string(bulb_control, 120, 1000, 1000)
        mock_bulb.set_multiple_values.assert_called_with({'21': 'music', '27': expected_dp27_string}, nowait=True)

    def test_generate_dp27_string(self):
        # Test with known values
        dp27_string = generate_dp27_string(None, 120, 1000, 1000, 'gradient')
        self.assertEqual(dp27_string, '0007803e803e800000000')

if __name__ == '__main__':
    unittest.main()
