import unittest

from cuts.line_slot import mill_line_slot
from tests.UnitTest import UnitTest


class LineSlotUnitTest(UnitTest):

    def test_basic(self):
        self.gcode.start()
        mill_line_slot(self.gcode, 0, 50, 0, 50, -5, 0, contract_mill_radius=True)
        self.gcode.finish()

    def test_expanded_x(self):
        self.gcode.start()
        mill_line_slot(self.gcode, 0, 50, 0, 0, -1, 0, contract_mill_radius=True)
        self.gcode.retract()
        mill_line_slot(self.gcode, 0, 50, 5, 5, -1, 0)
        self.gcode.retract()
        mill_line_slot(self.gcode, 0, 50, 10, 10, -1, 0, expand=3)
        self.gcode.finish()

    def test_expanded_xy(self):
        self.gcode.start()
        mill_line_slot(self.gcode, 0, 50, 0, 50, -1, 0, contract_mill_radius=True)
        self.gcode.retract()
        mill_line_slot(self.gcode, 0, 50, 0, 50, -2, -1)
        self.gcode.retract()
        mill_line_slot(self.gcode, 0, 50, 0, 50, -3, -1, expand=3)
        self.gcode.finish()

    def test_shifted(self):
        s = self.gcode.mill_radius
        self.gcode.start()
        mill_line_slot(self.gcode, 0, 50, 0, 50, -2, 0)
        self.gcode.retract()
        mill_line_slot(self.gcode, 0, 50, 0, 50, -2, 0, shift=self.gcode.mill_radius)
        self.gcode.retract()
        mill_line_slot(self.gcode, 0, 50, 0, 50, -2, 0, shift=self.gcode.mill_radius * 2)
        self.gcode.finish()

    def test_start_closest(self):
        self.gcode.start()
        mill_line_slot(self.gcode, 0, 50, 0, 50, -1, 0)
        self.gcode.home_xy()
        mill_line_slot(self.gcode, 50, 0, 56, 6, -1, 0)
        self.gcode.home_xy()
        mill_line_slot(self.gcode, 50, 0, 62, 12, -1, 0, start_closest=False)
        self.gcode.finish()

    def test_tabbed(self):
        self.gcode.start()
        mill_line_slot(self.gcode, 0, 50, 10, 60, -6, 0, tabs=True)
        self.gcode.finish()

    def test_tabbed_segmented(self):
        self.gcode.start()
        mill_line_slot(self.gcode, 0, 50, 0, 0, -1, 0, tabs=True)
        self.gcode.retract()
        dt = mill_line_slot(self.gcode, 0, 8.5, 5, 5, -1, 0, start_closest=False, tabs=True, dt=0)
        dt = mill_line_slot(self.gcode, 8.5, 43, 5, 5, -1, 0, start_closest=False, tabs=True, dt=dt)
        __ = mill_line_slot(self.gcode, 43, 50, 5, 5, -1, 0, start_closest=False, tabs=True, dt=dt)
        self.gcode.finish()


if __name__ == '__main__':
    unittest.main()
