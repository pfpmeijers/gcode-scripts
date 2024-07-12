import config
from utils.main import main_call
from circle_slot import create_circle_slot


def create_circle_pocket(xc: float, yc: float, zb: float, zt: float, r: float, zr: float = None):

    re = r - config.MILL_DIAMETER / 2
    r = config.WIDTH_OF_CUT
    while r < re:
        create_circle_slot(xc, yc, zb, zt, r)
        r += config.WIDTH_OF_CUT
    create_circle_slot(xc, yc, zb, zt, re)


if __name__ == "__main__":

    main_call(create_circle_pocket)
