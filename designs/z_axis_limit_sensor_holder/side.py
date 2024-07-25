import sys; sys.path.append('../../')

from common import *
from GCode import select_tool
from cuts.rect_pocket import create_rect_pocket

X1 = 8
X2 = 12

Y1 = -1.5
Y2 = -2
Y3 = -6
Y4 = -6.5

Z1 = -1.5

select_tool()

# P1
create_rect_pocket(xl=0 - config.MILL_DIAMETER / 2, xr=X2, yf=Y3, yb=Y2, zb=Z1, zt=0)

# P2
create_rect_pocket(xl=X1 - config.MILL_DIAMETER / 2, xr=X2 + config.MILL_DIAMETER / 2, yf=Y4, yb=Y1, zb=Z1, zt=0)
