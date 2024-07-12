import sys; sys.path.append('../../')

from common import *
from gcode import select_tool
from hole import create_hole
from rect_pocket import create_rect_pocket


select_tool()
create_rect_pocket(DXC - DXP1 / 2, DXC + DXP1 / 2, -config.MILL_DIAMETER / 2, DYP1, -DZP1, 0)
create_rect_pocket(DXC - DXP2 / 2, DXC + DXP2 / 2, DYB - DYP2 - config.MILL_DIAMETER / 2,
                   DYB + config.MILL_DIAMETER / 2, -DZP2, 0)
create_hole(DXB / 2 - DXH, DYB / 2, -DZS, -DZS + DZB)
create_hole(DXB / 2 + DXH, DYB / 2, -DZS, -DZS + DZB)
