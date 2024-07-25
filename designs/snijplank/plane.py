import sys; sys.path.append('../../')

from GCode import select_tool
from cuts.rect_pocket import create_rect_pocket

import config
config.WIDTH_OF_CUT = 10

select_tool()
create_rect_pocket(0, 330, 0, 394, -0.1, 0)
