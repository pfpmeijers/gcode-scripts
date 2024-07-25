from cuts.basics import retract, approach, plunge
from utils.main import main_call


def mill_hole(x: float, y: float, zb: float, zt: float):

    approach(x, y, zt)
    plunge(zb)


def create_hole(x: float, y: float, zb: float, zt: float):

    retract()
    mill_hole(x, y, zb, zt)
    retract()


if __name__ == "__main__":

    main_call(create_hole)
