import sys; sys.path.append('../../')

from common import *
from gcode import select_tool
from rect_pocket import create_rect_pocket
from line_slot import create_x_line_slot, create_y_line_slot

X1 = 4
X2 = 7.5
X3 = 14.5
X4 = 18.5
X5 = 27.5

Y1 = 4
Y2 = 6
Y3 = 12

Z1 = -3.5
Z2 = -9.5
Z3 = -13.5

select_tool()

# P1
create_rect_pocket(xl=0, xr=X4, yf=0 + M, yb=Y3, zb=Z1, zt=0, contract_mill_radius=True, expand=D)

# P2
create_rect_pocket(xl=X1, xr=X4 + D - M, yf=0 - (D - M), yb=Y3 + (D - M), zb=Z2, zt=Z1)

# P4
create_x_line_slot(xl=X2, xr=X3,
                   y=Y2,
                   zb=Z3 - M, zt=Z2)

# P3
create_y_line_slot(x=X4 + R,
                   yf=0, yb=Y3,
                   zb=Z3, zt=Z1,
                   expand=D - M,
                   tabs=True)

# P5
create_x_line_slot(xl=0, xr=X4,
                   y=Y3 + R,
                   zb=Z3, zt=Z1,
                   expand=D - M,
                   tabs=True)
