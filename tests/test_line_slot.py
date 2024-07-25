import unittest

from cuts.line_slot import create_line_slot
from tests.UnitTest import UnitTest


class LineSlotUnitTest(UnitTest):

    def test_basic(self):
        self.gcode.start()
        create_line_slot(self.gcode, 0, 50, 0, 50, -5, 0, contract_mill_radius=True)
        self.gcode.finish()

    def test_shifted(self):
        self.gcode.start()
        create_line_slot(self.gcode, 0, 50, 0, 50, -2, 0)
        create_line_slot(self.gcode, 0, 50, 0, 50, -2, 0, shift=self.gcode.config.mill.diameter)
        self.gcode.finish()

    def test_tabbed(self):
        self.gcode.start()
        create_line_slot(self.gcode, 0, 50, 0, 50, -6, 0, tabs=True)
        self.gcode.finish()


if __name__ == '__main__':
    unittest.main()
