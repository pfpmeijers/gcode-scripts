import sys; sys.path.append('../../')

from common import *
from GCode import select_tool
from cuts.rect_pocket import create_rect_pocket

X1 = -4
X2 = -23
X3 = -34
X4 = -53
X5 = -60

Y1 = 2.5
Y2 = 3
Y3 = 7
Y4 = 7.5

Z1 = -1.5

select_tool()

# P1
create_rect_pocket(xl=X5 - M, xr=D, yf=Y2, yb=Y3, zb=Z1, zt=0)

# P2
create_rect_pocket(xl=X4, xr=X3, yf=Y1, yb=Y4, zb=Z1, zt=0)

# P2
create_rect_pocket(xl=X2, xr=X1, yf=Y1, yb=Y4, zb=Z1, zt=0)
