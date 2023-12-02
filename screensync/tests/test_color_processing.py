import unittest
from unittest.mock import patch, MagicMock
from screen_sync.color_processing import get_screen_center, capture_screen_center, adjust_color, process_screen_color

class TestColorProcessing(unittest.TestCase):

    @patch('screen_sync.color_processing.ImageGrab.grab')
    def test_get_screen_center(self, mock_grab):
        # Mock the screen size
        mock_screen = MagicMock()
        mock_screen.size = (1920, 1080)
        mock_grab.return_value = mock_screen

        # Test the function
        bbox = get_screen_center((100, 100))
        self.assertEqual(bbox, (910, 490, 1010, 590))

    @patch('screen_sync.color_processing.ImageGrab.grab')
    @patch('screen_sync.color_processing.get_screen_center')
    def test_capture_screen_center(self, mock_get_screen_center, mock_grab):
        # Set up the mock
        mock_get_screen_center.return_value = (910, 490, 1010, 590)
        mock_image = MagicMock()
        mock_grab.return_value = mock_image

        # Test the function
        captured_image = capture_screen_center()
        mock_grab.assert_called_with(bbox=(910, 490, 1010, 590))
        self.assertEqual(captured_image, mock_image)

    def test_adjust_color(self):
        # Test with actual color values
        r, g, b = 100, 100, 100
        saturation_factor = 1.5
        adjusted_color = adjust_color(r, g, b, saturation_factor)
        self.assertTrue(isinstance(adjusted_color, tuple))
        self.assertEqual(len(adjusted_color), 3)

    def test_process_screen_color(self):
        # Mock functions
        with patch('screen_sync.color_processing.get_screen_center', return_value=(910, 490, 1010, 590)), \
             patch('screen_sync.color_processing.ImageGrab.grab'), \
             patch('screen_sync.color_processing.get_average_color', return_value=(100, 150, 200)), \
             patch('screen_sync.color_processing.adjust_color', return_value=(120, 130, 140)):

            # Test the function
            h, s, v = process_screen_color()
            self.assertTrue(isinstance(h, int) and isinstance(s, int) and isinstance(v, int))

if __name__ == '__main__':
    unittest.main()
