import unittest

from cuts.rect_pocket import create_rect_pocket
from tests.UnitTest import UnitTest


class RectPocketUnitTest(UnitTest):

    def test_single_lane_single_layer(self):
        self.gcode.start()
        create_rect_pocket(self.gcode, 0, 50, 0, 6, -1, 0, contract_mill_radius=True)
        self.gcode.finish()

    def test_multi_lane_single_layer(self):
        self.gcode.start()
        create_rect_pocket(self.gcode, 0, 50, 0, 50, -1, 0, contract_mill_radius=True)
        self.gcode.finish()

    def test_multi_lane_multi_layer(self):
        self.gcode.start()
        create_rect_pocket(self.gcode, 0, 50, 0, 50, -5, 0, contract_mill_radius=True)
        self.gcode.finish()

    def test_contracting_rects(self):
        self.gcode.start()
        create_rect_pocket(self.gcode, 0, 50, 0, 50, -5, 0, contract_mill_radius=True, meander=False)
        self.gcode.finish()


if __name__ == '__main__':
    unittest.main()
