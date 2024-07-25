import sys; sys.path.append('../../')

from common import *
from GCode import select_tool
from cuts.circle_pocket import create_circle_pocket
from cuts.fillet_rect_block import create_fillet_rect_block
from cuts.rounded_rect_slot import create_rounded_rect_slot

select_tool()
create_fillet_rect_block(0, DXB, 0, DYB, -DZS + config.TAB_HEIGHT, -DZS + DZB, 0, RH)
create_circle_pocket(DXC - DXH, DYC, -DZS, -DZS + DZB, RH)
create_circle_pocket(DXC + DXH, DYC, -DZS, -DZS + DZB, RH)
create_rounded_rect_slot(0, DXB, 0, DYB, -DZS, -DZS + config.TAB_HEIGHT, RH)

# Note: When aligning on left pocket, then zero at its center, move to (-(DXC - DXH), -DYC), and re-zero.
