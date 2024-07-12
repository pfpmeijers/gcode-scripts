from basics import retract, approach
from utils.main import main_call
from ramp import mill_circle_ramp


def mill_circle_slot(xc: float, yc: float, zb: float, zt: float, r: float):

    x = xc - r
    y = yc
    z = zt
    approach(x, y, z)
    while z > zb:
        z = mill_circle_ramp(xc, yc, z, zb, r)
    mill_circle_ramp(xc, yc, z, zb, r)


def create_circle_slot(xc: float, yc: float, zb: float, zt: float, r: float):

    retract()
    mill_circle_slot(xc, yc, zb, zt, r)
    retract()


if __name__ == "__main__":

    main_call(create_circle_slot)
