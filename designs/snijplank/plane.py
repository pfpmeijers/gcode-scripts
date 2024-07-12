import sys; sys.path.append('../../')

import presets.wood_4mm_flat
from gcode import select_tool
from hole import create_hole
from rect_pocket import create_rect_pocket

import config
config.WIDTH_OF_CUT = 10

select_tool()
create_rect_pocket(0, 330, 0, 394, -0.1, 0)
