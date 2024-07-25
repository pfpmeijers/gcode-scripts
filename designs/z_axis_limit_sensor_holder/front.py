import sys; sys.path.append('../../')

from common import *
from GCode import select_tool
from cuts.rect_pocket import create_rect_pocket

X1 = 12.5
X2 = 15

Y1 = 4.5
Y2 = 9
YM = 0.1  # Margin, not to cut out too far into the target assy

Z1 = -15

select_tool()

# P1
create_rect_pocket(xl=X1 - config.MILL_DIAMETER / 2, xr=X2 + config.MILL_DIAMETER / 2, yf=Y1 + YM, yb=Y2 - YM,
                   zb=Z1 - config.MILL_DIAMETER / 2, zt=0)
