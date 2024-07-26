import unittest
from math import sin, acos

from cuts.arc_slot import mill_arc_slot
from tests.UnitTest import UnitTest


class ArcSlotUnitTest(UnitTest):

    def test_basic(self):
        self.gcode.start()
        mill_arc_slot(self.gcode, 0, 50, 0, 50, -5, 0, 50)
        self.gcode.finish()

    def test_expanded(self):
        self.gcode.start()
        mill_arc_slot(self.gcode, 0, 50, 0, 50, -1, 0, 50, contract_mill_radius=True)
        self.gcode.retract()
        mill_arc_slot(self.gcode, 0, 50, 0, 50, -2, -1, 50)
        self.gcode.retract()
        mill_arc_slot(self.gcode, 0, 50, 0, 50, -3, -1, 50, expand=3)
        self.gcode.finish()

    def test_shifted(self):
        self.gcode.start()
        mill_arc_slot(self.gcode, 0, 50, 0, 50, -2, 0, 50)
        self.gcode.retract()
        mill_arc_slot(self.gcode, 0, 50, 0, 50, -2, 0, 50, shift=self.gcode.mill_radius)
        self.gcode.retract()
        mill_arc_slot(self.gcode, 0, 50, 0, 50, -2, 0, 50, shift=self.gcode.mill_radius * 2)
        self.gcode.finish()

    def test_start_closest(self):
        self.gcode.start()
        mill_arc_slot(self.gcode, 0, 50, 0, 50, -1, 0, 50)
        self.gcode.home_xy()
        mill_arc_slot(self.gcode, 44, -6, 56, 6, -1, 0, 50, clockwise=False)
        self.gcode.home_xy()
        mill_arc_slot(self.gcode, 38, -12, 62, 12, -1, 0, 50, clockwise=False, start_closest=False)
        self.gcode.finish()

    def test_tabbed(self):
        self.gcode.start()
        mill_arc_slot(self.gcode, 0, 50, 10, 60, -6, 0, 50, tabs=True)
        self.gcode.finish()

    def test_tabbed_segmented(self):
        self.gcode.start()
        x1, x2 = 8, 45
        y1, y2 = sin(acos((50 - x1)/ 50)) * 50, sin(acos((50 - x2) / 50)) * 50
        dt = mill_arc_slot(self.gcode, 0, x1, 0, y1, -1, 0, 50, start_closest=False, tabs=True, dt=0)
        dt = mill_arc_slot(self.gcode, x1, x2, y1, y2, -1, 0, 50, start_closest=False, tabs=True, dt=dt)
        __ = mill_arc_slot(self.gcode, x2, 50, y2, 50, -1, 0, 50, start_closest=False, tabs=True, dt=dt)
        self.gcode.finish()


if __name__ == '__main__':
    unittest.main()
