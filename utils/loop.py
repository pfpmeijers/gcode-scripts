import config


def loop_z(zb: float, zt: float, dz: float = None):

    if dz is None:
        dz = config.DEPTH_OF_CUT

    z = zt
    zp = None
    while True:
        z = max(z - dz, zb)
        if z == zp:
            break
        zp = z
        yield z
