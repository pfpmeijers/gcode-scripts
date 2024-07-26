import unittest

from cuts.circle_slot import mill_circle_slot
from tests.UnitTest import UnitTest


class CircleSlotUnitTest(UnitTest):

    def test_basic(self):
        self.gcode.start()
        mill_circle_slot(self.gcode, 5, 5, -5, 0, 50)
        self.gcode.finish()

    def test_tabbed(self):
        self.gcode.start()
        mill_circle_slot(self.gcode, 5, 5, -5, 0, 50, tabs=True)
        self.gcode.finish()


if __name__ == '__main__':
    unittest.main()
