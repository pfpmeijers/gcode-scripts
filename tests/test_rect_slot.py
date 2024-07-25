import unittest

from cuts.rect_slot import create_rect_slot
from tests.UnitTest import UnitTest


class RectSlotUnitTest(UnitTest):

    def test_basic(self):
        self.gcode.start()
        create_rect_slot(self.gcode, 0, 50, 0, 25, -5, 0)
        self.gcode.finish()

    def test_tabbed(self):
        self.gcode.start()
        create_rect_slot(self.gcode, 0, 50, 0, 25, -6, 0, tabs=True)
        self.gcode.finish()


if __name__ == '__main__':
    unittest.main()
