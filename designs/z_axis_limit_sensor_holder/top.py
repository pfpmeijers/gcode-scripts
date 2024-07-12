import sys; sys.path.append('../../')

from common import *
from gcode import select_tool
from circle_pocket import create_circle_pocket
from rect_pocket import create_rect_pocket
from line_slot import create_x_line_slot

X1 = 15
X2 = 18.5
X3 = 24.5
X4 = 27.5

Y0 = -3
Y1 = 6
Y2 = 12
Y3 = 15

Z1 = -1.5
Z2 = -4
Z3 = -6.75
Z4 = -9
Z5 = -12

R1 = 1.6

select_tool()
# P1
create_rect_pocket(xl=0, xr=X4, yf=Y0, yb=Y3, zb=Z1, zt=0)

# P2
create_rect_pocket(xl=X1, xr=X4, yf=0 - config.MILL_DIAMETER / 2, yb=Y2 + config.MILL_DIAMETER / 2, zb=Z2, zt=Z1)

# P3
create_rect_pocket(xl=X1, xr=X3, yf=0 - config.MILL_DIAMETER / 2, yb=Y2 + config.MILL_DIAMETER / 2, zb=Z4, zt=Z2)

# P4
create_circle_pocket(xc=X2,
                     yc=Y1,
                     zb=Z5, zt=Z4,
                     r=R1)

# P5
create_x_line_slot(xl=0, xr=X4,
                   y=Y0 + config.MILL_DIAMETER / 2,
                   zb=Z3, zt=Z1,
                   expand=config.MILL_DIAMETER / 2)

# P6
create_x_line_slot(xl=0, xr=X4,
                   y=Y3 - config.MILL_DIAMETER / 2,
                   zb=Z3, zt=Z1,
                   expand=config.MILL_DIAMETER / 2, tabs=True)