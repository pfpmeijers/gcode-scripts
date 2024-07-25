import unittest

from cuts.rect_slot import create_rect_slot
from tests.UnitTest import UnitTest


class TransformationUnitTest(UnitTest):

    def test_rect_slot_xy(self):
        self.gcode.transformation.scale(0.5, 1)
        self.gcode.transformation.rotate_xy(25)
        self.gcode.transformation.translate(5, 5, 0)
        self.gcode.start()
        create_rect_slot(self.gcode, 0, 50, 0, 25, -6, 0, tabs=True)
        self.gcode.finish()

    def test_rect_slot_z(self):
        self.gcode.transformation.scale(1, 2)
        self.gcode.transformation.translate(0, 0, 3)
        self.gcode.start()
        create_rect_slot(self.gcode, 0, 50, 0, 25, -6, 0, tabs=True)
        self.gcode.finish()


if __name__ == '__main__':
    unittest.main()
