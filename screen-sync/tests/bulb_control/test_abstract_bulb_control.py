import unittest
from screen_sync.bulb_control.abstract_bulb_control import AbstractBulbControl

class ConcreteBulbControl(AbstractBulbControl):
    def connect(self):
        pass

    def set_color(self, r, g, b):
        pass

    def turn_off(self):
        pass

    def turn_on(self):
        pass

class TestAbstractBulbControl(unittest.TestCase):

    def test_subclass_must_implement_abstract_methods(self):
        bulb_control = ConcreteBulbControl()
        self.assertIsInstance(bulb_control, AbstractBulbControl)
        # Test the methods
        bulb_control.connect()
        bulb_control.set_color(255, 255, 255)
        bulb_control.turn_off()
        bulb_control.turn_on()

if __name__ == '__main__':
    unittest.main()
